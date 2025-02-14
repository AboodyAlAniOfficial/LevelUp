# LevelUp

## Documentation Instructions

We are using Markdown files to create our documentation, as they can be stored in our git repository and edited and reviewed by the same means as our code.

To turn a markdown file into a pdf, we can use the program [Pandoc](https://pandoc.org/).  Run the following command to turn the markdown file `doc.md` into `doc.pdf`:

```shell
pandoc doc.md -o doc.pdf --variable colorlinks=true
```

Don't bother storing PDF files in the repository; that's just a waste of space and they can easily be created with the command.

Here is a guide to Markdown syntax, in case anyone needs it:  
[The Markdown Guide](https://www.markdownguide.org/)
