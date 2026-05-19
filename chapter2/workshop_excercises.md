# Chapter 2 - Working inside workspace

You have an existing repository that we will be working in. First let's ask Copilot how to run this application.

It may guess that it uses `uv`, but it takes some time to find this information out.
But the worst case scenario, it will try to run the application differently and try
to resolve potential errors with workarounds instead of using correct option.

> ### Task
>
> Add information that this project uses `uv` to run application and manage depedencies. What is the best place to do so?

## Explore the repository

First let's install the following skill: [Acquire Codebase Knowledge](https://awesome-copilot.github.com/skills/#file=skills%2Facquire-codebase-knowledge%2FSKILL.md).

To install it you should:
- download it
- unpack it
- copy the directory `acquire-codebase-knowledge` to `.github/skills/` directory

> ### Task
>
> Explore the repositroy. Let the Copilot explain the main purpouse of the code,
> how it is working and if there are any bugs.
>
> Did Copilot used the new skill? If not try to force it to use it with `/` command.
>
> If it found a bug, fix it.

## Add new feature to the codebase

The management likes the new dashboard, but they would like to see forcast for the next month regarding the future sales figures. This time you are task to leverage everything you learnd so far to try to add this feature.

> ### Task
>
> Add a script to traing a forcasting model (add any pacakges you need) that then
> can be used to predict the future sales figures.
>
> Add feature to the main application that displays the forcasts if there is a model
> that can predict it.
>
> Few question before starting:
> - How would you approach this?
> - How to split the work?
> - How to structure prompts?
> - Should you try to run everything at once?
> - How to explore data so that the Copilot knows how to design traning pipeline?

