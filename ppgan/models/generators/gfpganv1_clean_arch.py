#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
import random

import paddle
from paddle import nn
from paddle.nn import functional as F

from ppgan.models.generators.stylegan2_clean_arch import StyleGAN2GeneratorClean
from ppgan.models.generators.builder import GENERATORS


class StyleGAN2GeneratorCSFT(StyleGAN2GeneratorClean):
    """StyleGAN2 Generator with SFT modulation (Spatial Feature Transform).

    It is the clean version without custom compiled CUDA extensions used in StyleGAN2.

    Args:
        out_size (int): The spatial size of outputs.
        num_style_feat (int): Channel number of style features. Default: 512.
        num_mlp (int): Layer number of MLP style layers. Default: 8.
        channel_multiplier (int): Channel multiplier for large networks of StyleGAN2. Default: 2.
        narrow (float): The narrow ratio for channels. Default: 1.
        sft_half (bool): Whether to apply SFT on half of the input channels. Default: False.
    """

    def __init__(self,
                 out_size,
                 num_style_feat=512,
                 num_mlp=8,
                 channel_multiplier=2,
                 narrow=1,
                 sft_half=False):
        super(StyleGAN2GeneratorCSFT,
              self).__init__(out_size,
                             num_style_feat=num_style_feat,
                             num_mlp=num_mlp,
                             channel_multiplier=channel_multiplier,
                             narrow=narrow)
        self.sft_half = sft_half

    def forward(self,
                styles,
                conditions,
                input_is_latent=False,
                noise=None,
                randomize_noise=True,
                truncation=1,
                truncation_latent=None,
                inject_index=None,
                return_latents=False):
        """Forward function for StyleGAN2GeneratorCSFT.

        Args:
            styles (list[Tensor]): Sample codes of styles.
            conditions (list[Tensor]): SFT conditions to generators.
            input_is_latent (bool): Whether input is latent style. Default: False.
            noise (Tensor | None): Input noise or None. Default: None.
            randomize_noise (bool): Randomize noise, used when 'noise' is False. Default: True.
            truncation (float): The truncation ratio. Default: 1.
            truncation_latent (Tensor | None): The truncation latent tensor. Default: None.
            inject_index (int | None): The injection index for mixing noise. Default: None.
            return_latents (bool): Whether to return style latents. Default: False.
        """
        if not input_is_latent:
            styles = [self.style_mlp(s) for s in styles]
        if noise is None:
            if randomize_noise:
                noise = [None] * self.num_layers
            else:
                noise = [
                    getattr(self.noises, f'noise{i}')
                    for i in range(self.num_layers)
                ]
        if truncation < 1:
            style_truncation = []
            for style in styles:
                style_truncation.append(truncation_latent + truncation *
                                        (style - truncation_latent))
            styles = style_truncation
        if len(styles) == 1:
            inject_index = self.num_latent
            if styles[0].ndim < 3:
                latent = paddle.tile(styles[0].unsqueeze(1),
                                     repeat_times=[1, inject_index, 1])
            else:
                latent = styles[0]
        elif len(styles) == 2:
            if inject_index is None:
                inject_index = random.randint(1, self.num_latent - 1)
            latent1 = paddle.tile(styles[0].unsqueeze(1),
                                  repeat_times=[1, inject_index, 1])
            latent2 = paddle.tile(
                styles[1].unsqueeze(1),
                repeat_times=[1, self.num_latent - inject_index, 1])
            latent = paddle.concat([latent1, latent2], axis=1)
        out = self.constant_input(latent.shape[0])
        out = self.style_conv1(out, latent[:, 0], noise=noise[0])
        skip = self.to_rgb1(out, latent[:, 1])
        i = 1
        for conv1, conv2, noise1, noise2, to_rgb in zip(self.style_convs[::2],
                                                        self.style_convs[1::2],
                                                        noise[1::2],
                                                        noise[2::2],
                                                        self.to_rgbs):
            out = conv1(out, latent[:, i], noise=noise1)
            if i < len(conditions):
                if self.sft_half:
                    out_same, out_sft = paddle.split(out, 2, axis=1)

                    out_sft = out_sft * conditions[i - 1] + conditions[i]
                    out = paddle.concat([out_same, out_sft], axis=1)
                else:
                    out = out * conditions[i - 1] + conditions[i]
            out = conv2(out, latent[:, i + 1], noise=noise2)
            skip = to_rgb(out, latent[:, i + 2], skip)
            i += 2
        image = skip
        if return_latents:

            return image, latent
        else:
            return image, None


class ResBlock(nn.Layer):
    """Residual block with bilinear upsampling/downsampling.

    Args:
        in_channels (int): Channel number of the input.
        out_channels (int): Channel number of the output.
        mode (str): Upsampling/downsampling mode. Options: down | up. Default: down.
    """

    def __init__(self, in_channels, out_channels, mode='down'):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2D(in_channels, in_channels, 3, 1, 1)
        self.conv2 = nn.Conv2D(in_channels, out_channels, 3, 1, 1)
        self.skip = nn.Conv2D(in_channels, out_channels, 1, bias_attr=False)
        if mode == 'down':
            self.scale_factor = 0.5
        elif mode == 'up':
            self.scale_factor = 2

    def forward(self, x):
        out = paddle.nn.functional.leaky_relu(self.conv1(x), negative_slope=0.2)
        out = F.interpolate(out, scale_factor=self.scale_factor, mode= \
            'bilinear', align_corners=False)
        out = paddle.nn.functional.leaky_relu(self.conv2(out),
                                              negative_slope=0.2)
        x = F.interpolate(x, scale_factor=self.scale_factor, mode= \
            'bilinear', align_corners=False)
        skip = self.skip(x)
        out = out + skip
        return out


def debug(x):
    print(type(x))
    if isinstance(x, list):
        for i, v in enumerate(x):
            print(i, v.shape)
    else:
        print(0, x.shape)


@GENERATORS.register()
class GFPGANv1Clean(nn.Layer):
    """The GFPGAN architecture: Unet + StyleGAN2 decoder with SFT.

    It is the clean version without custom compiled CUDA extensions used in StyleGAN2.

    Ref: GFP-GAN: Towards Real-World Blind Face Restoration with Generative Facial Prior.

    Args:
        out_size (int): The spatial size of outputs.
        num_style_feat (int): Channel number of style features. Default: 512.
        channel_multiplier (int): Channel multiplier for large networks of StyleGAN2. Default: 2.
        decoder_load_path (str): The path to the pre-trained decoder model (usually, the StyleGAN2). Default: None.
        fix_decoder (bool): Whether to fix the decoder. Default: True.

        num_mlp (int): Layer number of MLP style layers. Default: 8.
        input_is_latent (bool): Whether input is latent style. Default: False.
        different_w (bool): Whether to use different latent w for different layers. Default: False.
        narrow (float): The narrow ratio for channels. Default: 1.
        sft_half (bool): Whether to apply SFT on half of the input channels. Default: False.
    """

    def __init__(self,
                 out_size,
                 num_style_feat=512,
                 channel_multiplier=1,
                 decoder_load_path=None,
                 fix_decoder=True,
                 num_mlp=8,
                 input_is_latent=False,
                 different_w=False,
                 narrow=1,
                 sft_half=False):
        super(GFPGANv1Clean, self).__init__()
        self.input_is_latent = input_is_latent
        self.different_w = different_w
        self.num_style_feat = num_style_feat
        unet_narrow = narrow * 0.5
        print("unet_narrow", unet_narrow, "channel_multiplier",
              channel_multiplier)
        channels = {
            '4': int(512 * unet_narrow),
            '8': int(512 * unet_narrow),
            '16': int(512 * unet_narrow),
            '32': int(512 * unet_narrow),
            '64': int(256 * channel_multiplier * unet_narrow),
            '128': int(128 * channel_multiplier * unet_narrow),
            '256': int(64 * channel_multiplier * unet_narrow),
            '512': int(32 * channel_multiplier * unet_narrow),
            '1024': int(16 * channel_multiplier * unet_narrow)
        }

        self.log_size = int(math.log(out_size, 2))
        first_out_size = 2 ** int(math.log(out_size, 2))
        self.conv_body_first = nn.Conv2D(3, channels[f'{first_out_size}'], 1)
        in_channels = channels[f'{first_out_size}']
        self.conv_body_down = nn.LayerList()
        for i in range(self.log_size, 2, -1):
            out_channels = channels[f'{2 ** (i - 1)}']
            self.conv_body_down.append(
                ResBlock(in_channels, out_channels, mode='down'))
            in_channels = out_channels
        self.final_conv = nn.Conv2D(in_channels, channels['4'], 3, 1, 1)
        in_channels = channels['4']
        self.conv_body_up = nn.LayerList()
        for i in range(3, self.log_size + 1):
            out_channels = channels[f'{2 ** i}']
            self.conv_body_up.append(
                ResBlock(in_channels, out_channels, mode='up'))
            in_channels = out_channels
        self.toRGB = nn.LayerList()
        for i in range(3, self.log_size + 1):
            self.toRGB.append(nn.Conv2D(channels[f'{2 ** i}'], 3, 1))
        if different_w:
            linear_out_channel = (int(math.log(out_size, 2)) * 2 -
                                  2) * num_style_feat
        else:
            linear_out_channel = num_style_feat
        self.final_linear = nn.Linear(channels['4'] * 4 * 4, linear_out_channel)
        self.stylegan_decoder = StyleGAN2GeneratorCSFT(out_size=out_size,
                                                       num_style_feat=num_style_feat, num_mlp=num_mlp,
                                                       channel_multiplier=channel_multiplier, narrow=narrow, sft_half= \
                                                           sft_half)
        if decoder_load_path:
            self.stylegan_decoder.load_state_dict(
                paddle.load(decoder_load_path)['params_ema'])
        if fix_decoder:
            for _, param in self.stylegan_decoder.named_parameters():
                param.requires_grad = False
        self.condition_scale = nn.LayerList()
        self.condition_shift = nn.LayerList()
        for i in range(3, self.log_size + 1):
            out_channels = channels[f'{2 ** i}']
            if sft_half:
                sft_out_channels = out_channels
            else:
                sft_out_channels = out_channels * 2
            self.condition_scale.append(
                nn.Sequential(
                    nn.Conv2D(out_channels, out_channels, 3, 1, 1),
                    nn.LeakyReLU(0.2, True),
                    nn.Conv2D(out_channels, sft_out_channels, 3, 1, 1)))
            self.condition_shift.append(
                nn.Sequential(
                    nn.Conv2D(out_channels, out_channels, 3, 1, 1),
                    nn.LeakyReLU(0.2, True),
                    nn.Conv2D(out_channels, sft_out_channels, 3, 1, 1)))

    def forward(self,
                x,
                return_latents=False,
                return_rgb=True,
                randomize_noise=True):
        """Forward function for GFPGANv1Clean.

        Args:
            x (Tensor): Input images.
            return_latents (bool): Whether to return style latents. Default: False.
            return_rgb (bool): Whether return intermediate rgb images. Default: True.
            randomize_noise (bool): Randomize noise, used when 'noise' is False. Default: True.
        """
        conditions = []
        unet_skips = []
        out_rgbs = []
        feat = paddle.nn.functional.leaky_relu(self.conv_body_first(x),
                                               negative_slope=0.2)
        for i in range(self.log_size - 2):
            feat = self.conv_body_down[i](feat)
            unet_skips.insert(0, feat)
        feat = paddle.nn.functional.leaky_relu(self.final_conv(feat),
                                               negative_slope=0.2)
        style_code = self.final_linear(feat.reshape([feat.shape[0], -1]))
        if self.different_w:
            style_code = style_code.reshape(
                [style_code.shape[0], -1, self.num_style_feat])
        for i in range(self.log_size - 2):
            feat = feat + unet_skips[i]
            feat = self.conv_body_up[i](feat)
            scale = self.condition_scale[i](feat)
            conditions.append(scale.clone())
            shift = self.condition_shift[i](feat)
            conditions.append(shift.clone())
            if return_rgb:
                out_rgbs.append(self.toRGB[i](feat))

        image, _ = self.stylegan_decoder(styles=[style_code],
                                         conditions=conditions,
                                         return_latents=return_latents,
                                         input_is_latent=self.input_is_latent,
                                         randomize_noise=randomize_noise)
        if return_latents:
            return image, _
        else:
            return image, out_rgbs
