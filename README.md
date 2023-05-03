# Build a data pipeline Workflow with Temporal and Python

Temporal makes writing data pipelines easy with Workflows and Activities.

You can create a source, process the step or steps, and output the flow of information to a destination with just code. Meaning all of your developer best practices can be implemented, tested, and ran as needed.

That data that enters a Workflow is handled by Activities, while the Workflow orchestrates the execution of those steps.
You can ensure that Temporal handles all actions and executes it observably once, all in Python code.

In this tutorial, you'll learn to build a data pipeline that gets the top 10 Hacker New stories and processes the items based on the story ID.
If the API endpoint is down, the default behavior of the Retry Policy is to retry indefinitely.

You'll then implement a Schedule to Schedule Workflows on an interval to leverage the automation of running Workflow Executions.

## Step 0: Prerequisites

* Python >= 3.7
* [Poetry](https://python-poetry.org)
* [Local Temporal server running](https://docs.temporal.io/application-development/foundations#run-a-development-cluster)

With this repository cloned, run the following at the root of the directory:

```command
poetry install
```

# Start the Workflow

Start and run the Workflow with the following commands:

```command
# terminal one
poetry run python run_worker.py
# terminal two
poetry run python run_workflow.py
```

Terminate the Workflow with the following command:

```command
# terminal three
temporal workflow terminate --workflow-id temporal-community-workflow
```