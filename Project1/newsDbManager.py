#!/usr/bin/env python3

import newsViewTables
import psycopg2

DATABASE_NAME = "news"

QUERY_THREE_MOST_POPULAR_ARTICLES = """
    SELECT articles.title, top3_paths.view_count
        FROM articles, top3_paths
        WHERE articles.slug = top3_paths.log_slug
        ORDER BY top3_paths.view_count DESC;
"""

QUERY_FOUR_MOST_POPULAR_AUTHORS = """
    SELECT authors.name, top4_authors.view_count
        FROM authors, top4_authors
        WHERE authors.id = top4_authors.author;
"""

QUERY_DAYS_WITH_HIGH_ERRORS = """
    SELECT
        TO_CHAR(not_ok_req.day, 'MON DD, YYYY') AS day,
        ROUND
         ( ((not_ok_req.request_count / all_req.request_count) * 100)::DEC, 2 )
         AS error_req_ratio
    FROM
        not_ok_req, all_req
    WHERE
        not_ok_req.day = all_req.day
      AND
        ROUND
         ( ((not_ok_req.request_count / all_req.request_count) * 100)::DEC, 2 ) > 1.0
    ORDER BY error_req_ratio DESC;
"""

def run_query(query):
    """ Template function for running any query and returning the results. """
    db  = psycopg2.connect(database=DATABASE_NAME)
    cursor = db.cursor()
    for q in query:
        cursor.execute(q)
    result = cursor.fetchall()
    db.close()
    return result

def get_top_three_articles():
    """ Return the top three viewed articles. """
    return run_query([
                        newsViewTables.REMOVING_VIEWS_IF_THERE_ANY,
                        newsViewTables.VIEW_THREE_MOST_ACCESSED_ARTICLE_PATHS,
                        QUERY_THREE_MOST_POPULAR_ARTICLES
                    ])

def get_top_four_authors():
    """ Return the top four authors by their articles view count. """
    return run_query([
                        newsViewTables.REMOVING_VIEWS_IF_THERE_ANY,
                        newsViewTables.VIEW_FOUR_MOST_POPULAR_AUTHORS,
                        QUERY_FOUR_MOST_POPULAR_AUTHORS
                    ])

def get_days_with_highest_error_rates():
    """ Return the days with error rates > 1.0 of the total requests. """
    return run_query([
                        newsViewTables.REMOVING_VIEWS_IF_THERE_ANY,
                        newsViewTables.VIEW_NOT_OK_REQUESTS_PER_DAY,
                        newsViewTables.VIEW_ALL_REQUESTS_PER_DAY,
                        QUERY_DAYS_WITH_HIGH_ERRORS
                    ])
