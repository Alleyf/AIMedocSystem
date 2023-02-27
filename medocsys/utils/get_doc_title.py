from tika import parser


def get_pdf_title(title: str):
    url = '../../media/docs/' + title  # 测试
    # url = './media/docs/' + title + '.pdf'  # 实际
    print(url)
    parsedPDF = parser.from_file(url)
    if "pdf:docinfo:title" in parsedPDF['metadata']:
        # return parsedPDF['metadata']["pdf:docinfo:title"]
        return parsedPDF['metadata']  # 测试
    else:
        return title


if __name__ == '__main__':
    print(get_pdf_title("isct_a-118.pdf"))
