---
lineNumbers: true
download: true
theme: dracula
highlighter: shiki
favicon: '/favicon.png'
fonts:
  sans: "Barlow"
---

# **Aggregating data in Django using database views**

### a talk by Mikuláš Poul
### July 10th, 2024 - Europython

---

# About me

- he/him, go by Miki
- Born in the Czech Republic
- Live in London, UK

<v-clicks>

- Coding in Python for more years than not
- Have been using Django for 10 years
- Staff Engineer at [<img src="/xelix.svg" style="display: inline; height: 25px; margin-top: -10px" />](https://xelix.com/)
- [www.mikulaspoul.cz](https://www.mikulaspoul.cz/)

</v-clicks>

<!--
Mention all links & relevant details are on mikulaspoul, plus a blog and link to this talk
-->

---

# Motivation slide

- Intro [1m]
- Describe examples of aggregating data from django models [4m]
- Describe downsides of inbuilt django methods [5m]
- Introduce database views [5m]
- Introduce django-pgviews-redux library [2m]
- Show-off how to use the views from the library as models [5m]
- Describe trade-offs of database views [3m]
- Introduce materialized views [5m]

---

# Data Aggregation In Django

Descibe the two aggregation methods

.aggregate()
.values().annotate()

---

# Show example

User page visit
User summary stats

---

# What does the aggregation actually do

Talk about the SQL it generates

---

# Downsides of the django aggregation

Talk about it returning a dict
Displaying data has to be fairly manual

---

# Wanting to use the aggregation for more

Expose this to staff users or end users

---

# Describe VIEW

Behaves like table for SELECT
Evaluates every single time
Just syntactic sugar

---

# Enter django-pgviews-redux

Library maintained by me
Fork of earlier library
Support for modern python and django, with extra features
Postgres specific


---

# Using django-pgviews-redux

Define & sync views

--- 

# Use the view

Using normal queryset on it
Add methods
Admin
Serializer

---

# Cost to the view

Evaluates every single time

--- 

# Materialized View

Stores the query result in a temporary table
Any updates to underlying data -> out of date
Good for storing batch processes or when you don't care data is out of date
Bad when need to refresh often and data is big
Indexes

---

# Other view usages

Database de-normalisation
Expensive calculated values

---

# Conclusion

Add views to your reportaire 

---
layout: statement
---

# Questions?

---
layout: center
class: "text-center"
---

# Slides

TODO!

<img src="/qr_link.png" style="height: 300px" />

[Web](https://www.mikulaspoul.cz/talks/django-aggregation-talk/) / [Source](https://github.com/mikicz/django-aggregation-talk/)
