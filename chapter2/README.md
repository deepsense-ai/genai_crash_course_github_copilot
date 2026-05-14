---
marp: true
---

# Chapter 2 - AI coding for Hackaton

## Standard Training Materials

Presenter: Bartosz Mikulski

---

## Introduction

This chapter is about using AI coding agents effectively during a hackathon.

- We work under time pressure.
- We integrate unfamiliar APIs and tools.
- We need a working demo, not perfect architecture.

The goal is to use agents to move faster without losing control over the solution.

---

## What is Hackaton?

A hackathon is not just about writing code quickly.

It is about delivering value to users in a short time.

- combine multiple APIs and systems
- turn raw data into useful insights
- automate a real workflow
- build something demoable and practical

---

## How to leverage Vibe/agentic coding

Vibe coding is useful in hackathons because it accelerates the boring and repetitive parts.

Use agents to:

- scaffold a project quickly
- read docs and propose integrations
- generate API clients and glue code
- refactor rough code into a cleaner version
- debug obvious issues faster

Keep the human in charge of scope, tradeoffs, and verification.

---

# The prompts

---

## The prompts: Divide and conquer

Large prompts usually produce vague solutions.

Break the problem into smaller tasks:

- define the input
- fetch the data
- transform the data
- generate the output
- handle errors

Small, focused prompts are easier for the agent to solve well.

---

## The prompts: Planning mode

Planning mode helps before you start generating code.

Ask the agent to create a plan when the task:

- spans multiple files
- depends on several APIs
- has important edge cases
- needs sequencing between steps

This reduces rework and makes the implementation more predictable.

--- 

## The prompts: Exercise 1

Write a Python script that based on user location plots the forcasted temperature 
for the next 7 days. You should use https://open-meteo.com/ API to get the weather data.
You can use any plotting library you like and save the plot as an image file.

---

## The prompts: Be specific

Specific prompts produce better code because they reduce ambiguity.

- State the goal clearly.
- Name the libraries or tools you want to use.
- Describe the expected structure of the solution.
- Set constraints for style, complexity, and error handling.

The more precise the prompt, the less time you spend fixing the result.

---
## The prompts - Bad vs good: libraries

**Bad prompt**

> Build a weather chart app in Python.

**Why it fails**

- No API specified
- No plotting library specified
- No output format specified

**Good prompt**

> Write a Python script that uses the Open-Meteo API and `matplotlib` to fetch a 7-day temperature forecast for the user's location and save the chart as `forecast.png`.

---

## The prompts - Bad vs good: structure

**Bad prompt**

> Create a script that gets weather data.

**Why it fails**

- No guidance on functions or modules
- No separation of responsibilities
- Harder to test and extend

**Good prompt**

> Create a Python script with separate functions for geolocation lookup, weather API calls, and chart generation. Keep the entry point in `main()` and make the code easy to read.

---

## The prompts - Bad vs good: style and complexity

**Bad prompt**

> Write the shortest possible solution.

**Why it fails**

- Encourages dense, unclear code
- Often removes useful names and comments
- Optimizes for brevity instead of maintainability

**Good prompt**

> Write a beginner-friendly Python solution. Prefer readability over clever tricks, use descriptive variable names, add short comments only where needed, and avoid unnecessary abstractions.

---

## Bad vs good: error handling

**Bad prompt**

> Call the API and plot the result.

**Why it fails**

- Ignores network failures
- Ignores missing or invalid data
- Ignores user-facing error messages

**Good prompt**

> Handle HTTP errors, timeouts, and empty API responses gracefully. If data cannot be fetched, print a clear error message and exit without crashing.

---

## The prompts: Specificity checklist

When prompting an agent for code, specify:

- Goal: what should be built
- Inputs and outputs: files, CLI, API, UI
- Libraries and frameworks: what to use or avoid
- Structure: script, package, functions, tests
- Quality bar: readability, performance, simplicity
- Failure modes: validation, retries, logging, errors


--- 

## Exercise 2

You are given two directories: ex2-bad and ex2-good. Your task is to generate a
interactive report application that reads sales data and displays monthly revenue charts
split by category. Display also top 10 best performing salespeople.

---

### In ex2-bad use vague prompts like:
> Build a sales report app in Python.
> Get me insights about `sales_data.csv` and plot some charts. Make it interactive.

---

### In ex2-good use specific prompts like:

> Write a Python NiceGUI dashboard that shows monthly revenue charts by category and a table of the top 10 salespeople based on `../sales_data.csv`. 
> Keep the code organized, modular (you can use multiple files). Create a plan of implementation first. In case of doubts ask for clarification.
> You can explore the data first to get insights before development.

**Hint:** Ask agent to generate a summary of the data and save it to a file. 
That way you can reference it in your main prompt.

---

## Understanding the code with Agents

When you enter a new codebase, you can use agents to quickly understand the structure and logic.
Especially when the code is convoluted or poorly documented.

It is also good option to get a review for your own work, as well as to generate documentation.
In general exploring codebase with agents is a good way to get familiar with it before you start making changes.

---

## Exercise 3

You are given a legacy codebase in `ex3/legacy_code` directory. Your task is to understand how it works, detect flaws and suggest improvements. 

Finally use the agent to refactor the code into a cleaner, more modular version in `ex3/refactored_code` directory.
