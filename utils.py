import time

def merge(arr,start,mid,end,corresponding_arr=None):
	if corresponding_arr == None:
		corresponding_arr = arr
	new_arr = []
	corr_new_arr = []
	left_pivot = start
	right_pivot = mid + 1
	while left_pivot!=mid+1 and right_pivot!=end+1:
		if arr[left_pivot]<arr[right_pivot]:
			new_arr.append(arr[left_pivot])
			corr_new_arr.append(corresponding_arr[left_pivot])
			left_pivot += 1
		else:
			new_arr.append(arr[right_pivot])
			corr_new_arr.append(corresponding_arr[right_pivot])
			right_pivot += 1
	if left_pivot == mid+1:
		for i in range(right_pivot,end+1):
			new_arr.append(arr[i])
			corr_new_arr.append(corresponding_arr[i])
	else:
		for i in range(left_pivot,end+1):
			new_arr.append(arr[i])
			corr_new_arr.append(corresponding_arr[i])

	for i in range(end-start+1):
		arr[start+i] = new_arr[i]
		corresponding_arr[start+i] = corr_new_arr[i]

def merge_sort(arr, start, end, corresponding_arr=None):
	if start == end:
		return
	mid = (start + end)//2
	merge_sort(arr,start,mid,corresponding_arr)
	merge_sort(arr,mid+1,end,corresponding_arr)
	merge(arr,start,mid,end,corresponding_arr)

def find_date_number(date):
    day = int(date[0])
    year = int(date[2]) 
    months = {
        'January': 31,
        'February': 28 + int(year%4==0),
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30,
        'October': 31,
        'November': 30,
        'December':31,
    }
    date_number = 0
    for month, days in months.items():
        if month == date[1]:
            break
        date_number += days
    date_number += day + year * 365 + year//4
    return date_number

