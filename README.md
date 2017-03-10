# Jigsaw

Jigsaw is a wrapper for the [Jinja2](http://jinja.pocoo.org/docs/2.9/) templating system. When provided with data files `D`, and a template `t[x]`, Jigsaw computes `t[D]`.

## Installation
Jigsaw depends on the Python libraries `jinja2` and `yaml`. These can be installed through `pip` or `brew`.

After installing the dependencies, simply add the `jigsaw` folder to your `$PYTHONPATH`. You can then run Jigsaw by `python3 jigsaw ...`.

## Usage
Jigsaw takes at most three parameters, two of which are required:
* `-t`, or `--template`: the template files Jigsaw will use. Can be either a single file or a directory.
* `-d`, or `--data`: the data files Jigsaw will use. Can be either a single file or a directory.
* `-o`, or `--output`: the output target. If the argument to `--template` is a file, this output will be a file whose name is the `--output` argument. If the template file is a directory, then the output will be a directory with the provided name.

## Examples
Consider the files below:
```
template
|-- images
|   |-- ...
|-- src
|   |-- index.html
|   |-- projects.html
|   |-- ...
|-- ...
```
and
```
data
|-- main.yaml
|-- notes.yaml
|-- projects
|   |-- jigsaw.yaml
|   |-- ...
|-- ...
```
Running the command

`python3 jigsaw -t template -d data -o out`

will first load the `data` directory into a dictionary to pass to `jinja2` templates. If `@` denotes dictionary union and `<file>` denotes the dictionary representation of `file.yaml`, the dictionary representation of the `data` file is:

`<data> := <main> @ <notes> @ {projects: [<jigsaw> @ ...]} @ ...`

That is, the top-level directory is ignored, while sub-directories form dictionary entries whose keys are the name of the directory and whose values are a list of the sub-dictionaries.

Now, if `file.html <- <d>` denotes evaluating the template `file.html` with provided data dictionary `<d>`, the output of our entire script will be the directory
```
out
|-- images
|   |-- ...
|-- src
|   |-- index.html <- <data>
|   |-- projects.html <- <data>
|   |-- ...
|-- ...
```

## Currently supported filetypes
For data files, Jigsaw supports:
* yaml

For template files, Jigsaw supports:
* html
* LaTex
* markdown
* ...
