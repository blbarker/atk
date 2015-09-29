Examples
--------
Consider the following sample data set in *frame* with actual data labels
specified in the *labels* column and the predicted labels in the
*predictions* column:

# <setup>
>>> import trustedanalytics as ta
>>> ta.connect()
-etc-

>>> f = ta.Frame(ta.UploadRows([[1], [3], [1], [0], [2], [1], [4], [3]], [('numbers', ta.int32)]))
-etc-

# </setup>

# Given frame 'f'

>>> f.inspect()
[#]  numbers
============
[0]        1
[1]        3
[2]        1
[3]        0
[4]        2
[5]        1
[6]        4
[7]        3

>>> ecdf_frame = f.ecdf('numbers')
-etc-

>>> ecdf_frame.inspect()
[#]  numbers  numbers_ECDF
==========================
[0]        0         0.125
[1]        1           0.5
[2]        2         0.625
[3]        3         0.875
[4]        4           1.0

