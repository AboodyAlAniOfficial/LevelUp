# LevelUp

## Project Authors

This project was created by the following people:
- Abood Al-Ani (218938993) <aboodyaa@my.yorku.ca>  
- Nikhil Arora (220874947) <narora46@my.yorku.ca>  
- Adrien Hopkins (217267550) <ahopk127@my.yorku.ca>  
- Hamad Iqbal (217296393) <hamadi8@my.yorku.ca>  
- Bilal Jameel (216567380) <bilaljameel665@gmail.com>/<bilal665@my.yorku.ca>  
- Tan Khoa Tran (218060541) <rickt02@my.yorku.ca>

## Dependencies

- [PostgreSQL](https://www.postgresql.org/)

## Setup Instructions

These instructions assume you have already installed and setup the dependencies.  If not, do that.

### Database

To setup the database, simply:
1. Open `pgAdmin`.
2. Open the query tool (second icon on the left sidebar).
3. Select a server to use, then press "Connect & Open Query Tool".
4. In the new window that appears, open the file [schema.sql](./schema.sql).
5. Execute the script.

## Documentation Instructions

We are using Markdown files to create our documentation, as they can be stored in our git repository and edited and reviewed by the same means as our code.

To turn a markdown file into a pdf, we can use the program [Pandoc](https://pandoc.org/).  Run the following command to turn the markdown file `doc.md` into `doc.pdf`:

```shell
pandoc doc.md -o doc.pdf --variable colorlinks=true
```

Don't bother storing PDF files in the repository; that's just a waste of space and they can easily be created with the command.

Here is a guide to Markdown syntax, in case anyone needs it:  
[The Markdown Guide](https://www.markdownguide.org/)
