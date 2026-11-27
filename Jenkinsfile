pipeline {

    agent any

    environment {

        PROJECT_NAME = 'jenkins-fastapi-demo'

        PYTHON_BIN = '.venv/bin/python'

        REPORT_FILE = 'reports/junit.xml'
    }

    options {

        buildDiscarder(
            logRotator(numToKeepStr: '10')
        )

        disableConcurrentBuilds()

        skipDefaultCheckout(true)

        skipStagesAfterUnstable()

        disableRestartFromStage()

        timeout(
            time: 20,
            unit: 'MINUTES'
        )
    }

    parameters {

        booleanParam(
            name: 'BUILD_PACKAGE',
            defaultValue: true,
            description: 'Create ZIP package on main after successful tests'
        )
    }

    stages {

        stage('Checkout') {

            steps {

                echo '======================================'

                echo 'STAGE 1 - Checkout Source Code'

                echo '======================================'

                deleteDir()

                checkout scm

                script {

                    env.CI_BRANCH = env.BRANCH_NAME ?: (
                        env.JOB_NAME == 'day03-fastapi-pipeline'
                            ? 'main'
                            : 'unknown'
                    )
                }

                echo "Current Branch: ${env.CI_BRANCH}"

                echo "Build Number: ${env.BUILD_NUMBER}"

                sh '''#!/bin/bash
set -euo pipefail

echo "JOB_NAME=${JOB_NAME}"

echo "BUILD_NUMBER=${BUILD_NUMBER}"

echo "WORKSPACE=${WORKSPACE}"

echo "CI_BRANCH=${CI_BRANCH}"

echo "Current User:"
whoami

echo "Current Git Commit:"
git log -1 --oneline

echo "Project Files:"
ls -lah
'''
            }
        }

        stage('Install') {

            steps {

                echo '======================================'

                echo 'STAGE 2 - Install Dependencies'

                echo '======================================'

                sh '''#!/bin/bash
set -euo pipefail

mkdir -p reports dist

echo "Create Python Virtual Environment"

python3 -m venv .venv

echo "Python Version"

"$PYTHON_BIN" --version

echo "Install Dependencies"

"$PYTHON_BIN" -m pip install -r requirements-dev.txt

echo "Validate Dependencies"

"$PYTHON_BIN" -m pip check
'''
            }
        }

        stage('Test') {

            steps {

                echo '======================================'

                echo 'STAGE 3 - Automated Tests'

                echo '======================================'

                sh '''#!/bin/bash
set -euo pipefail

mkdir -p reports

echo "Run pytest for ${CI_BRANCH}"

"$PYTHON_BIN" -m pytest -v --junitxml="$REPORT_FILE"

echo "Validate Test Report"

test -s "$REPORT_FILE"

ls -lh reports/
'''
            }

            post {

                always {

                    script {

                        if (fileExists(env.REPORT_FILE)) {

                            junit(
                                testResults: env.REPORT_FILE,
                                allowEmptyResults: false
                            )

                        } else {

                            echo 'JUnit report was not generated.'
                        }
                    }
                }
            }
        }

        stage('Package') {

            when {

                allOf {

                    expression {
                        return env.CI_BRANCH == 'main'
                    }

                    expression {
                        return params.BUILD_PACKAGE
                    }
                }
            }

            steps {

                echo '======================================'

                echo 'STAGE 4 - Package Application'

                echo '======================================'

                sh '''#!/bin/bash
set -euo pipefail

mkdir -p dist

test -s "$REPORT_FILE"

PACKAGE_NAME="${PROJECT_NAME}-${BUILD_NUMBER}.zip"

export PACKAGE_NAME

SOURCE_COMMIT="$(git rev-parse HEAD)"

export SOURCE_COMMIT

echo "Create Application ZIP Package"

git archive --format=zip --output="dist/${PACKAGE_NAME}" HEAD

echo "Validate ZIP Package"

unzip -t "dist/${PACKAGE_NAME}"

echo "Generate Build Metadata"

"$PYTHON_BIN" - <<'PY'
import json
import os

from datetime import datetime, timezone
from pathlib import Path

from app import APP_VERSION


build_info = {
    "project": os.environ["PROJECT_NAME"],
    "application_version": APP_VERSION,
    "git_branch": os.environ["CI_BRANCH"],
    "job_name": os.environ["JOB_NAME"],
    "build_number": os.environ["BUILD_NUMBER"],
    "git_commit": os.environ["SOURCE_COMMIT"],
    "artifact": os.environ["PACKAGE_NAME"],
    "created_at": datetime.now(
        timezone.utc
    ).isoformat(),
}


output_file = Path("dist/build-info.json")


with output_file.open(
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        build_info,
        file,
        ensure_ascii=False,
        indent=4,
    )

    print(file=file)


print(output_file.read_text(encoding="utf-8"))
PY

echo "Generated Artifacts"

ls -lh dist/
'''
            }
        }
    }

    post {

        always {

            echo '======================================'

            echo 'Pipeline Post Actions'

            echo '======================================'
        }

        success {

            script {

                if (
                    env.CI_BRANCH == 'main' &&
                    params.BUILD_PACKAGE
                ) {

                    archiveArtifacts(
                        artifacts: 'dist/*.zip,dist/build-info.json,reports/junit.xml',
                        fingerprint: true,
                        allowEmptyArchive: false,
                        onlyIfSuccessful: true
                    )

                } else {

                    archiveArtifacts(
                        artifacts: 'reports/junit.xml',
                        allowEmptyArchive: false,
                        onlyIfSuccessful: true
                    )
                }
            }

            echo 'Pipeline completed successfully.'
        }

        failure {

            echo 'Pipeline failed. Check Console Output.'
        }

        unstable {

            echo 'Pipeline completed with an UNSTABLE result.'
        }

        aborted {

            echo 'Pipeline was aborted.'
        }

        cleanup {

            echo "JOB_NAME: ${env.JOB_NAME}"

            echo "BUILD_NUMBER: ${env.BUILD_NUMBER}"

            echo "GIT_BRANCH: ${env.CI_BRANCH ?: 'unknown'}"

            echo "FINAL RESULT: ${currentBuild.currentResult}"
        }
    }
}
