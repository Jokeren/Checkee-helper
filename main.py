#!/bin/python

import numpy as np
import sys
import logging
import matplotlib.pyplot as plt
import matplotlib.dates
import datetime
import collections

def plot2d(x, y, xticks, xlabel, ylabel, title, path):
  plt.plot(x, y)
  plt.xticks(x, xticks, rotation='vertical')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.grid(True)
  plt.title(title)
  plt.savefig(path + ".png")

def count_check_days(array, location):
  days_dict = collections.OrderedDict()
  date_dict = {}
  for i in xrange(array.shape[0]):
    if location == array[i, 4] or location == '':
      date = datetime.datetime.strptime(array[i, 7], "%Y/%m/%d").strftime("%Y-%m-%d")
      if date in days_dict:
        days_dict[date] += float(array[i, 9])
        date_dict[date] += 1.0
      else:
        days_dict[date] = float(array[i, 9])
        date_dict[date] = 1.0

  days = np.empty(len(days_dict))
  dates = np.empty(len(days_dict), dtype="object")
  size = 0

  for key in days_dict:
    dates[size] = key
    days[size] = days_dict[key] / date_dict[key]
    size += 1

  plot2d(xrange(len(days_dict)), days, dates, "Date", "Days", "Check days", "check days")

def count_pass_rate(array, location):
  pass_dict = collections.OrderedDict()
  date_dict = {}
  for i in xrange(array.shape[0]):
    if location == array[i, 4] or location == '':
      date = datetime.datetime.strptime(array[i, 7], "%Y/%m/%d").strftime("%Y-%m-%d")
      if date in pass_dict:
        date_dict[date] += 1.0
        if array[i, 6] == "Clear":
          pass_dict[date] += 1.0
      else:
        date_dict[date] = 1.0
        if array[i, 6] == "Clear":
          pass_dict[date] = 1.0

  passes = np.empty(len(pass_dict))
  dates = np.empty(len(pass_dict), dtype="object")
  size = 0

  for key in pass_dict:
    dates[size] = key
    passes[size] = pass_dict[key] / date_dict[key]
    size += 1

  plot2d(xrange(len(pass_dict)), passes, dates, "Date", "Pass", "Pass rate", "pass rate")

def main(argv=None):
  if argv is None:
    argv = sys.argv

  if len(argv) < 3:
    logging.error("not enough arguments")
    exit(1)
  
  main_function = argv[1]
  main_file = argv[2]

  main_location = ''
  if len(argv) >= 4:
    main_location = argv[3]

  array = np.loadtxt(main_file, delimiter=',', dtype='str')

  if main_function == "days":
    check_days = count_check_days(array, main_location)
  elif main_function == "rate":
    pass_rate = count_pass_rate(array, main_location)
  else:
    logging.error("no " + main_function + " function!")
    exit(1)

if __name__ == "__main__":
  sys.exit(main())
