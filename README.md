# pfda2dockstore

Export precisionFDA apps to Dockstore

The script `pfda2dockstore` exports a specific app, apps from a provided list, or all the apps that are public on
[precisionFDA](https://precision.fda.gov/).

For each exported app the script will create:
 * a repo in Github to store the source files (CWL descriptor, Dockerfile),
 * a repo in DockerHub, where the image will be pushed,
 * a repo in Dockstore.
The Dockstore org (namespace), GitHub org, and DockerHub org are set to `pfda2dockstore` by default
in the runner script. The Dockstore repos are not published.

## Running pfda2dockstore

You can set the following variables in your environment. Another option is to provide them when prompted
when the helper (runner) script is executed.

* PFDA_TOKEN (your PrecisionFDA access token)
* GITHUB_TOKEN (your GitHub access token)
* DS_TOKEN (your Dockstore access token)

You can also prepare the environment:

```
    conda create -n pfda python=3.5 anaconda
    source activate pfda
    pip install PyGithub agithub yaml
```

### Export a specific app

In order to export one app, run `run.sh`. The script will prompt you for an app name and for the tokens if they
are not set in the script or in the environment.

```
    ./run.sh
```

Alternatively, you can call the `pfda2dockstore` script from the command line. For example, to export
[vcf-comparison](https://precision.fda.gov/apps/app-BqB9XZ8006ZZ2g5KzGXP3fpq) and
save it in Github at [pfda2dockstore](https://github.com/pfda2dockstore) and DockerHub
organization [pfda2dockstore](https://hub.docker.com/u/pfda2dockstore):

```
    $ docker login
    $ python pfda2dockstore --app-name vcf-comparison \
                            --pfda-token $PFDA_TOKEN \
                            --dockstore-token $DS_TOKEN
                            --github-token $GITHUB_TOKEN \
                            --github-org pfda2dockstore \
                            --dockerhub-org pfda2dockstore \
                            --dockstore-org pfda2dockstore
```

The most recent version (i.e. one with the largest revision number) will be exported. If there exists an repo in
GitHub or in Dockstore with the same name the script will return an error. The repos will need to be removed before
retrying.

### Export all apps

To export all the (public) apps from precisionFDA to Dockstore, run the script:

```
    ./run_export_apps.sh
```

A list of apps that were *not* successfully registered on Dockstore will be returned at the end of the execution. You
can re-run the export of these apps using an "export from list" option below.

It's a good idea to tee the standard error and output messages to a file for inspection later:

```
    ./run_export_apps.sh 2>&1 | tee pfda2dockstore.log
```

### Export apps from a list

You can also export only a subset of apps, provided as a list in a file. In order to do so, create a file with app names,
one per line, for example:

```
    $ cat > my_apps.txt
      url-fetcher
      bai
```

and run:

```
    ./run_export_apps.sh my_apps.txt
```

The apps from this list will be exported. A list of apps that were *not* successfully registered will be returned
at the end of the execution.

## Results

After the execution take a look at your org in Github, DockerHub, and Dockstore.
You should see the example `vcf-comparison` repo (or whichever tool you chose to export).

