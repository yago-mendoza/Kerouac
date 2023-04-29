# Kerouac

## Table of contents

* [General Information](#general-information)
* [Time-Saving Features](#time-saving-features)
* [Installation](#installation)
* [Usage](#usage)

## General Information

This software application is a console-based database management tool, allowing users to effortlessly develop and traverse a graph structure of interconnected nodes, each node representing a specific syntagma.

The program's ability to seamlessly explore and modify the connections between nodes within the graph can assist in improving the coherence and consistency of written content, making it more effective and impactful for their intended purpose. Furthermore, the use of an application can facilitate the development of language[^1] proficiency by providing a platform for practical experimentation with diverse linguistic elements. Through such experimentation, users can engage in active learning, acquiring and refining language skills in context.

[^1]: It should be noted that the current database used by the program is written in Spanish, but the tool itself can be applied to any language or any other ontological relational system.

### Node interconnexions

Node interconnections play a crucial role in comprehending the relationships between different particles. The database is designed to distinguish between synonymical connections, which represent similarities in meaning, and semantical connections, which capture direct relationships based on various factors such as usage, context, or classification.

### Context

This project is a simplified version of Ebadgi, which is designed to provide temporary access to the Süskind, McKee, and Kelsey databases, included in the project as a foundational component. Although the development of an specific API for these databases has been halted, the database development itself is still ongoing. This prototype provides access to the most fundamental functionalities, temporarely.

## Time-Saving Features

For editing the database, the tool offers a variety of commands that allow users to add, delete, and modify nodes as needed. Users can transfer data between nodes, and easily navigate the database to import specific data to a node. The tool also enables users to navigate synonyms, semantics, and notes attributes. Notes contain both definitions, examples, and additional commentaries.

In addition to editing the database, the tool enables users to consult individual nodes. By inputting the name of a node, users can view its attributes, including its synonyms, semantics, and notes. This allows users to quickly access information about specific linguistic elements without needing to navigate the entire database.

Furthermore, the tool implements a variable called BATCH that enables fast searches. With this feature, users can search for multiple nodes at once by inputting a list of node names. The tool will then output the attributes of each node in the list, making it easy to compare and analyze multiple linguistic elements at once. This feature saves users time and improves efficiency in their research and analysis.

## Installation

Assuming that you already have [git](https://git-scm.com/downloads/) and [python3](https://www.python.org/downloads/) installed on your system, to download all the files and folders from a GitHub repository to your local machine, you can use the `git clone` command followed by the URL of the repository. In this case, the command is:

```bash
git clone https://github.com/yago-mendoza/Kerouac
```

This will create a new directory called "Kerouac" in your current working directory, which will contain all the files and folders from the repository.

Once you have cloned the repository, you can run the `console.py` file using Python. To do this, navigate to the "Kerouac" directory that was created when you cloned the repository, and then run the following command:

```python
py console.py
```

This script contains the code for the program, which allows you to interact with a database using a command-line interface, displaying the following program header.

```
~ KEROUAC ~
Contact : yagomendoza.dev@gmail.com
Tip : write "help" to learn more about commands.
<i> .autosave : 'False' by default
```

And Congrats 🎉 the Application would start if you have followed each step correctly. This will allow you to easily explore and modify the linguistic graph using a variety of commands, such as "cd node," "ls node," or "remove node", further developed in the [next section](#usage). The application is designed to be user-friendly, with simple and intuitive commands that allow you to navigate and modify the graph with ease. It also includes error-handling features to prevent accidental modifications and ensure that the program runs smoothly.

## Usage

After every action, the prompt `%H.%M.%S ~ [field]@[node]/:` indicates the current node and the layer of interconnexions currently targeted, either "synonymical" or "semantical". Additionally, there is a 3rd field dedicated to "Observations" which provides a space to store custom input such as definitions, examples, or fun facts related to the node.

### Commands

#### Basic Commands
The following is a list of basic commands that can be used to navigate the database:

* `e/y/o` : switches the "attribute field" to synonyms, semantics or observations.
* `cd <title>` : sets the "current node" to a specified node.
* `r (--pinned)` : sets the "current node" to a random node.
* `cd ..` : sets the "current node" to the previous one.
* `.remove` : deletes the "current node" from the database.
* `p` : pins the "current node".
* `u` : unpins the "current node".
* `[custom text]` : associates custom text to the working "attribute field" for the "current node".
* `= <i> <i> ...` : updates the attributes for the current "attribute field" with those of the specified attribute.
* `<i> <i> ... =` : transfers the "attribute field" attributes of the "current node" to those at specified positions.
* `ls / + (sort)` : displays the set "attribute field" for the current node.

#### Batch Commands
The batch is a space for storing nodes for performing searches. The following is a list of batch commands:

* `<` : adds the "current node" to the batch.
* `< <title>` : adds a specified node to the batch.
* `> <i> <i> ...` : empties the specified nodes from the batch.
* `>>` : empties the batch completely.
* `b (sort)` : displays the batch.
* `*<n>` : effectuates a search based on at least "n" batch attributes.

#### Suggester Commands
The suggester allows for quick navigation through intelligent attributes, allowing for further study or immediate insertion:

* `s` : instantiates a suggester and accesses it.
* `''` : generates the next suggestion.
* `t` : associates the current suggestion with the "current node" through the set "attribute field".
* `cd` : sets the current suggestion to the "current node".
* `<` : adds the suggestion to the batch.
* `c` : rints out the "current node" expression.
* `ls / + (sort)` : displays the set "attribute field" for the suggestion (purely optical)
* `q` : quits suggester mode.

#### Other Commands
The following is a list of miscellaneous commands:

* `~ <title> :` finds and displays grammatically similar nodes.
* `&pinned (sort)` : displays all favorite (pinned) nodes.
* `$obs` : generates a random observation.
* `:ncol <n>` : sets the number of displaying columns to "n".
* `:autosave (0/1)` : toggles between auto-save and manual-save.
* `:details (0/1)` : toggles between showing details (number of connections) when displaying node lists or not.
* `.clear` : clears the window.
* `.extract` : saves a copy of the database to the desktop environment.
* `.save` : saves the progress so far.
* `.exit` : quits the terminal (discards any unsaved changes).

#### Attribute Displays
Before expiring (bash will report it), attribute displays (ls/+) implement the following commands:

* `cd <i>` : sets the "current node" to the specified attribute.
* `del <i> <i> ...` : deletes the specified connections.
* `ls <i>` : displays the "attribute field" for the specified attribute, streamlining navigation.
* `del` : deletes all attributes from the "attribute field" at the "current

### Errors

#### Unspecifed arguments
`<!> Error 200` : field to be set ("y"/"e"/"o"). <br />
`<!> Error 201` : no node set as current yet. <br />
`<!> Error 202` : undetermined suggester ("y"/"e"). <br />
#### Missing data
`<!> Error 300` : data-pointer expired recently and indexes are no longer callable. <br />
`<!> Error 301` : history is empty. <br />
`<!> Error 302` : node is not yet in the database. <br />
`<!> Error 303` : the inserted node does not exist. <br />
#### Syntax control
`<!> Error 400` : invalid command. <br />
`<!> Error 401` : specified indexes out of range. <br />
`<!> Error 402` : current node cannot be found in the database yet. <br />
`<!> Error 403` : the flexibility parameter for the search must be numeric and unique. <br />
`<!> Error 404` : attributes must be at least 2 characters long. <br />
`<!> Error 405` : first character must always be capitalized. <br />
`<!> Error 406` : observations cannot be assigned in bulk. <br />
`<!> Error 407` : observations cannot be accessed like nodes. <br />
#### Other errors
`<!> Error 505` : could not save database to desktop path. <br />

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

Distributed under the MIT License. See [MIT](https://choosealicense.com/licenses/mit/) for more information.

## Contact Me

If you want to contact me, you can
reach me at yagomendoza.dev@gmail.com
