# coding:utf-8
import pandas as pd


def merge_col(frame, func=None, symbol=''):
    """
    主要是功能是将多列按某种方式拼接在一起，然后在进行func操作
    比如工作常用的，将某三列A、B、C在中间加下划线方式拼接，然后转MD5,则调用方式如下
    merge_col(frame=df[['A','B','C']], func=MD5_encode, symbol='_')
    :return: Series format

    """
    row, col = frame.shape
    if col < 2:
        raise Exception(u'DataFrame至少两列以上才能拼接')

    ret = frame.apply(lambda x: symbol.join(map(str, x)), axis=1)
    return ret.apply(func) if func else ret


if __name__ == '__main__':

    df = pd.DataFrame(data=[['A', 'B', 3, 'R'], ['T', 'Y', 9, 'P']], columns=['a', 'b', 'c', 'd'])
    print merge_col(df, str.lower, '_')

