# Airflow Demo

Airflow is a workflow engine from Airbnb. Airbnb developed it for its internal use and had open sourced it. In Airflow, the workflow is defined programmatically. Airflow document says that it's more maintainable to build workflows, and Airflow also comes with a elegant web interface. 

The main concept of airflow is a DAG (Directed Acyclic Graph). A DAG contains vertices and directed edges. In a DAG, you can never reach to the same vertex, at which you have started, following the directed edges. Otherwise your workflow can get into an infinite loop. In workflow context, tasks can be defined as vertex and the sequence is represented with the directed edge. The sequence decides the order in which the tasks will be performed.

Make no mistake about the fact that airflow is just a workflow engine. It is only responsible for defining tasks and sequences. The details of task has to be handled by each task on its own. Airflow provides hooks for initiating tasks and has integration points to other systems.

Airflow is in Python and the workflows are also defined using Python. 

## Install

Airflow needs a home and we can give the home to any place.

```
# assume you checkout the repo and change to the folder
export AIRFLOW_HOME=`pwd`
```

### Install airflow

`pip install airflow`

### Initialize database

`airflow initdb`

### Start the webserver

`airflow webserver -p 8080`

### Start the scheduler

The Airflow scheduler monitors all tasks and all DAGs, and triggers the task instances whose dependencies have been met. Behind the scenes, it monitors and stays in sync with a folder for all DAG objects it may contain, and periodically (every minute or so) inspects active tasks to see whether they can be triggered.

The Airflow scheduler is designed to run as a persistent service in an Airflow production environment. To kick it off, all you need to do is execute `airflow scheduler`. It will use the configuration specified in `airflow.cfg`.

## Writing a DAG definition file

This Airflow Python script is just a configuration file specifying the DAG’s structure as code. The actual tasks defined here will run in a different context from the context of this script. Different tasks run on different workers at different points in time, which means that this script cannot be used to cross communicate between tasks.

People sometimes think of the DAG definition file as a place where they can do some actual data processing - that is not the case at all! The script’s purpose is to define a DAG object. It needs to evaluate quickly (seconds, not minutes) since the scheduler will execute it periodically to reflect the changes if any.

Let's write a workflow in the form of a DAG. We will have six task t1~t6. t2~t4 will depend on t1, t5 will depend on t2~t4 and t6 will depend on t5. Let's name the script demo.py and put it in dags folder of airflow home.

## Testing a DAG definition file

Time to run some tests. First let’s make sure that the pipeline parses. Let’s assume we’re saving the code from the previous step in demo.py in the DAGs folder referenced in your airflow.cfg.

`python dags/demo.py`

If the script does not raise an exception it means that you haven’t done anything horribly wrong, and that your Airflow environment is somewhat sound.

## Enabling a DAG definition file

Open any browser and visit default web server at http://localhost:8080, you should see the DAG `demo` is disabled.

![](https://raw.githubusercontent.com/jonascheng/AirflowDemo/master/screenshots/demo_dag_disabled.png)

Once you enable the DAG `demo`, all scheduled tasks will be catched up by default from 2017-03-01 on.

![](https://raw.githubusercontent.com/jonascheng/AirflowDemo/master/screenshots/demo_dag_enabled.png)

## Reference

* [Airflow Official Docs](https://airflow.incubator.apache.org/index.html)
* [Airflow - Beginners Tutorial](http://tech.lalitbhatt.net/2016/04/airflow-beginners-tutorial.html)

