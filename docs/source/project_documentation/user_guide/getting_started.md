# Getting Started as a User

## Github Template Repository - Quickstart
We have a [Github Template Repository](https://github.com/Coffee2Bits/AaC-User-Template-Repository) that's setup to allow users exploring AaC to immediately create an AaC-ready github repository and development environment using [Gitpod](https://gitpod.io/new/#https://github.com/DevOps-MBSE/AaC).

The repository is pre-populated with a simple example model and Github Action workflow. All that you have to do is hit the "Use this Template" button at the top of the template repository. ![Use this Template Button Picture](../../images/github/github_repo_template_button.png)

Alternatively, if you're opposed to visiting the template repository and searching for the template button, you can just click this one.

[Generate my AaC Github Repo](https://github.com/Coffee2Bits/AaC-User-Template-Repository/generate)

## Installing AaC
If you're not using a prepared environment, then you will need to install AaC and its Python dependencies. AaC is written in Python to help make it more approachable for casual users and easily extensible for power users.
**You will need Python 3.9 or later to run AaC.**

To install AaC on Linux, Windows, or macOS:
```bash
pip install aac
```

Usage information is available from the command line interface:
```bash
aac --help
```

Installed `aac` executable version information is available via  the `version` command:
```bash
aac version
```

AaC user features, any command that you use, are managed and implemented via a plugin system. If you want to add or extend the features of the AaC package, all you need to do is install a plugin or build it yourself. This allows us to maintain a small footprint for each user feature while providing the ability for users to completely customize their tooling and environment to their needs.

## Built-in AaC Commands
AaC does have two universal commands that are always available:
- validate:  Ensures your model is correctly defined per the AaC DSL
- version: Get the version of the AaC package installed

## First-Party Plugins
First-party plugins are user features that are built and maintained by the AaC development team. They receive first-class support such as unit and functional tests within the AaC repository and CI/CD pipeline. These plugins are special because they are **ALWAYS** packaged with the AaC package.

Some exmaples of first-party plugins are:
* Generate JSON representations of AaC models/files
* Generate PlantUML Diagrams
* Generate Protobuf3 Messages
* Generate markdown design documents
* Generate Gherkin Test files
* Numerous language validation plugins
  * Required fields are present
  * Root keys are defined


## Third-Party Plugins
Third-party plugins are plugins built by third-party developers and are outside the control of the AaC development team. These third party plugins have to be installed via pip in order to correctly register the plugin's command and functionality.

### Installing Plugins
Installing third-party plugins is easy with pip.

To install an AaC Plugin on Linux, Windows, or macOS:
```bash
pip install <aac-plugin>
```

If the plugin provides new command functionality you will see the new command(s) details in the usage information. If the expected commands aren't showing up then it's likely the plugin wasn't installed correctly.
```bash
aac --help
```

## Using AaC to Model Your System
The general pattern for decomposing whatever you want to model in AaC is begin by asking a few questions of the system, and correlate what aspects you want to define to corresponding AaC YAML entries, also referred to as AaC definitions.

For example:
* If you want to define a thing you would create a `model` definition
* If you want to define a data structure you would create a `schema` definition
* If you want to define an interface for something (models) you would populate the `behavior` field in your `model`
* If you want to define an interaction between your things (models) you would create a `usecase` definition incorporating the steps and actors in that interaction

## Defining Your First Model
Because AaC is an MBSE tool, `model` is a pretty central item to define. Let's start with an example of modeling an alarm clock. We can create a model for our overall alarm clock system/model by creating a new file in an AaC environment with the following content:
_alarm_clock.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/alarm_clock.yaml
    :language: yaml
    :lines: 6-8
```

Now, if you run the validation command:
`aac validate alarm_clock.yaml` you'll see a message indicating that your model is valid.

That's fairly simplistic, let's decompose our alarm clock system into components -- what parts make up our alarm clock? Let's say that there are three parts to our alarm clock, the internal clock, the timer for the alarm, and the alarm itself. We can define those three components as models that are components of our `AlarmClock` model like so:

_alarm_clock.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/alarm_clock.yaml
    :language: yaml
    :lines: 6-15, 38-41, 49-52, 73-76
```

Once again, we can check to confirm that this model is valid. Even better, we can use something this simple to start driving value. We can generate a simple object diagram by using the first-party plugin GenPlantUML with the command `aac puml-object alarm_clock.yaml diagrams` which will generate a file with the following PlantUML content:

_diagrams/object/alarm_clock_alarm_clock.puml_
```plantuml
@startuml  Object Diagram
title  Object Diagram
object AlarmClock
object Clock
object ClockTimer
object ClockAlarm
AlarmClock *-- Clock
AlarmClock *-- ClockTimer
AlarmClock *-- ClockAlarm
@enduml
```

More interestingly, this PlantUML diagram produces the following graphic when rendered:
![alarm clock PlantUML object diagram](../../images/alarm_clock/alarm_object_puml.png)

## Defining a Data Structure
Now that we have a basic alarm clock and some components, we can start defining the data structures that will be used in our example model. What better data for an alarm clock than a timestamp? We can define our timestamp data structure with the `schema` tag like so:

_structures.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/structures.yaml
    :language: yaml
    :lines: 13-29
```

Defining a data structure by itself isn't particularly useful, but we can reference this data structure in our models to define state or interfaces.

If we return to our alarm clock model, we can define that the timer component is stateful -- the function of the timer is influenced by the time provided by the user. This is easily defined by giving the `ClockTimer` model some state that includes the timestamp we just defined.

_alarm_clock.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/alarm_clock.yaml
    :language: yaml
    :lines: 50-56
    :emphasize-lines: 5-6
```

## Defining Model Interfaces
Data structures are also used when defining interfaces between models/components of your system. What these interfaces translate to is highly dependent upon your needs and which plugins you're using. For instance, the GenProtobuf plugin identifies the data structures defined in `model.behavior` fields and generates Protobuf3 equivalent messages of those data structures for use in software messaging/communication.

If we return to our alarm clock example, then we can define the interface to our alarm system. In this example we'll re-use the timestamp data structure for simplicity since it fairly represents the data that we'd expect a user to provide to an alarm clock:

_alarm_clock.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/alarm_clock.yaml
    :language: yaml
    :lines: 6-22
```

If we were to generate a component diagram from our model at this point, we'll be able to visualize the components and interfaces of our alarm clock model.

If we run the command `aac puml-component alarm_clock.yaml diagrams` to generate a component diagram, the resulting diagram will render to something like this:
![alarm clock PlantUML component diagram](../../images/alarm_clock/alarm_component_puml.png)

## Defining the Interactions Between Models
Finally, we can also model the interactions between our models; say that we want to define the scenario when a user sets the time on the alarm clock. These interactions are defined by using the `usecase` root key, listing the actors in our `usecase` under `usecase.participants`, and the steps that are involved in the `usecase` under `usecase.steps`.

For example, if we were to model the usecase of a user setting the alarm on our alarm clock, it might look something like:

Note the use of `import` to make definitions in separate files accessible to the current definitions.

_usecase.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/usecase.yaml
    :language: yaml
    :lines: 1-24
    :emphasize-lines: 1-4, 6, 9, 16
```

The file `external.yaml` has a simple model definition for our external user, who is an actor external to our system but one that we are referencing. Since we aren't focusing on modeling things external to our alarm clock, we can keep our `Person` model very simple.

_external.yaml_
```{eval-rst}
.. literalinclude:: ../../../../python/model/alarm_clock/external.yaml
    :language: yaml
```

With that usecase defined, we can generate a PlantUML sequence diagram `aac puml-sequence usecase.yaml diagrams`, which renders to:

![alarm clock PlantUML sequence diagram](../../images/alarm_clock/alarm_sequence_puml.png)

Voila! You've covered the basic parts of Architecture-as-Code!
