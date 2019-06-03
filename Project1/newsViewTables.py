#!/usr/bin/env python3

""" This file contains all of needed views to run the reporting tool. """

REMOVING_VIEWS_IF_THERE_ANY = """
    DROP VIEW IF EXISTS top3_paths;
    DROP VIEW IF EXISTS top4_authors;
    DROP VIEW IF EXISTS not_ok_req;
    DROP VIEW IF EXISTS all_req;
"""

VIEW_THREE_MOST_ACCESSED_ARTICLE_PATHS = """
    CREATE VIEW top3_paths AS
        SELECT SUBSTRING(path, 10) AS log_slug, COUNT(*) AS view_count
            FROM log
            GROUP BY path
            ORDER BY view_count DESC
            LIMIT 3 OFFSET 1;
"""

VIEW_FOUR_MOST_POPULAR_AUTHORS = """
    CREATE VIEW top4_authors AS
        SELECT articles.author, COUNT(log.id) AS view_count
            FROM articles, log
            WHERE SUBSTRING(log.path, 10) = articles.slug
            GROUP BY articles.author
            ORDER BY view_count DESC
            LIMIT 4;
"""

VIEW_NOT_OK_REQUESTS_PER_DAY = """
    CREATE VIEW not_ok_req AS
        SELECT DATE(time) AS day, CAST(COUNT(*) AS FLOAT) AS request_count
            FROM log
            WHERE status != '200 OK'
            GROUP BY day
            ORDER BY request_count DESC;
"""

VIEW_ALL_REQUESTS_PER_DAY = """
    CREATE VIEW all_req AS
        SELECT DATE(time) AS day, CAST(COUNT(*) AS FLOAT) AS request_count
            FROM log
            GROUP BY day
            ORDER BY request_count DESC;
"""
