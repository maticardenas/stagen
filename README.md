# Static Site Generator

This is a simple static site generator that I wrote in Python. It takes a directory of markdown files and generates a static site from them. 

## Features

- [x] Markdown to HTML conversion
- [x] Directory structure to URL mapping

## Usage

Content of your website in markdown format should be placed in the `content` directory. The directory structure will be preserved in the generated site.
There should always be a `index.md` file in each directory (including the root directory) to serve as the homepage of that directory.

To generate the site, run the following command:

```bash
main.sh
```

The generated site will be placed in the `public` directory and serve in port 8888.

## Tests

You can run the tests of the site itself by running the following command:

```bash
test.sh
```