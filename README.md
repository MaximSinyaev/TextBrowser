# Python based Text-browser
Project from [hyperskill](https://hyperskill.org).
In this project you'll have to create a toy browser that will ignore JS and CSS, won't have cookies and only will show a limited set of tags. But it will be enough for some situations. And it must be fun at least!

Used modules:

     - Requests
     - BeautifulSoup4
     - Colorama

## Examples of work
```shell script
$ ./text_browser.py
Directory for tabs: ./tabs (default: "./tabs")
Welcome to text-browser, hope you are here only because of interest!
For help type (help) or help
> help
Type url that you want to visit using full address (i.e. https://pypi.org) to display all staticreadable information from web-site.

Allowed commands:
     url   - display parsed web-page from the URL if possible
    (back) - display previous web-page
    (exit) - exits from browser
    (help) - shows this message

>  https://pypi.org
Skip to main content
Start the survey!
Help
Donate
Log in
Register
Help
Donate
Log in
Register
Find, install and publish Python packages with the Python Package Index
browse projects
204,651 projects
1,539,423 releases
2,293,550 files
(... and more such strings)
> exit
Goodbye
```
     