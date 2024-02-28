// Wesley and Mikas
// April 2023
// CSCI 324 Rust Creative Project
// Parser for a latex-like markdown language
// to use: cargo run in_file.md out_file.html

#[macro_use]
extern crate lalrpop_util;
use lalrpop_util::ParseError;

use std::env; //Command line arguments

use std::io::prelude::*;
use std::fs::OpenOptions; // file writing
use std::fs::File;

//The next line is to allow rust to automatically generate debug implementations, these impl are needed to
// to use the Result, unwrap, and the error default error handling
// The enum is used by the parser generator for errors in addition to the ones it provides ie invalid token etc
//We don't make the best use as we only have one error, but more could be used 
#[derive(Debug)]
pub enum Errors {
    UnknownCommand(String),
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert!(args.len() == 3, "2 Arguments expected. Please provide run with inputfile.md outputfile.html");
    let infile = &args[1];
    let outfile = &args[2];

    let mut f = File::open(infile)
        .expect("Failed to open file, ensure that it exists and can be read");
    // puts the file into a string
    let mut read_doc = String::new();
    f.read_to_string(&mut read_doc)
        .expect("failed to read file");

    // macro that puts the generated parser in scope
    lalrpop_mod!(pub markdown);
    let doc = markdown::DocumentParser::new().parse(&read_doc);
    match doc {
        Ok(doc) => {
            let mut file = OpenOptions::new()
                .write(true)
                .create_new(true) //fails if file already exists
                .open(outfile)
                .expect(&format!("Failed to create {} ensure you have rw permissions and that there is not already a file there", outfile));

            writeln!(file, "{doc}")
                .expect("Error writting to document");
            println!("Your document, {}, has been converted and saved as {}.", infile, outfile);
        },
        Err(error) => {
            println!("Oh no! An error has occurred when parsing {}: ", infile);
            println!("{}",
                match &error {
                    // We specified this error in our grammar, if we made our grammar more complex and specified more errors these could be matched here
                    ParseError::User { error: Errors::UnknownCommand(command) } => format!("Unknown Command: {command}"),
                    other => format!("{:?}", other),
                }
            )
        }
    }
}