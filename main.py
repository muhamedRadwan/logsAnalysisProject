#!/usr/bin/env python

import webapp2
import jinja2
import os
import psycopg2 as psycopg2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RedirectHandler):
    def write_form(self, *a, **kw):
        self.response.out.write(*a, **kw)

    @staticmethod
    def render_str(template, **args):
        t = jinja_env.get_template(template)
        return t.render(args)

    def render(self, template, **args):
        self.write_form(self.render_str(template, **args))


class MainHandler(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        user_choice = self.request.get("res")
        lis = []
        if user_choice == 'first':
            output = select_query('select * from numOFaccessArticales '
                                  'order by num desc  limit 3;')
            for o in output:
                s = list(o)
                s[1] = str(s[1]) + " views"
                lis.append(s)
        elif user_choice == 'second':
            output = select_query(' select name ,sum(num) as views '
                                  'from AuthorsWithSlug'
                                  ' group by name order by views desc ;')
            for o in output:
                s = list(o)
                s[1] = str(s[1]) + " views"
                lis.append(s)
        elif user_choice == 'third':
            output = select_query(' select * from PrecentageOFRequests '
                                  ' where errors>1 ;')
            for o in output:
                s = list(o)
                s[1] = str(s[1])+"% errors"
                lis.append(s)
        else:
            lis = None
        self.render("index.html", n=lis)


def select_query(query):
    """Return all posts from the 'database', most recent first."""
    conn = psycopg2.connect("dbname=news")
    cu = conn.cursor()
    cu.execute(query)
    rows = cu.fetchall()
    conn.close()
    return rows

app = webapp2.WSGIApplication([
    ('/', MainHandler)
        ], debug=True)


def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    main()
