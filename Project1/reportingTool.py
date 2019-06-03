#!/usr/bin/env python3

import newsDbManager


def report_maker():
    """ Reporting ... """
    solve_question_1()

    print("")
    solve_question_2()

    print("")
    solve_question_3()


def solve_question_1():
    print("Q1. What are the most popular three articles of all time?")
    articles = newsDbManager.get_top_three_articles()
    for article in articles:
        print("{:} - {:} views".format(article[0], article[1]))


def solve_question_2():
    print("Q2. Who are the most popular article authors of all time?")
    authors = newsDbManager.get_top_four_authors()
    for author in authors:
        print("{:<23} - {:>7} views".format(author[0], author[1]))


def solve_question_3():
    print("Q3. On which days did more than 1% of requests lead to errors?")
    days = newsDbManager.get_days_with_highest_error_rates()
    for day in days:
        print("{:} - {:}% errors".format(day[0], day[1]))


if __name__ == '__main__':
    report_maker()
else:
    print('Importing is not allowed. You should run it directly.')
