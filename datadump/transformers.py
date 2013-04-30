#!/usr/bin/python2.5
#
# Copyright: 	Longsystem Inc.
# Author:	Mike Huang
#
from datetime import datetime, date


#convert a single date string to date
def toDate(datestring):
    #Unsupported type datetime.date
    #return datetime.strptime(datestring,fmt).date()
    return datetime.strptime(datestring,fmt)
   
#convert a list of date strings to list of date
def toDateList(format,delimiter):
    global fmt
    fmt = format
    def to_date_list(value):       
        return map(toDate,value.split(delimiter))
    return to_date_list
   
#convert a single date to string
def dateToString(dt):
    return dt.strftime(fmt)

#convert list of dates to a single string
def dateListToString(format,delimiter):
    global fmt
    fmt = format
    def date_list_to_string(value):
        dateStringList = map(dateToString,value)
        return delimiter.join(dateStringList)
    return date_list_to_string



	