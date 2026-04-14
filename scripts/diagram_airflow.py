"""Airflow 워크플로우 플랫폼 아키텍처 다이어그램.

Airflow 도입(2025.03-2026.01) 프로젝트의
통합 후 아키텍처를 시각화한다.
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import Athena, GlueDataCatalog
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Tableau

import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

with Diagram(
    "",
    filename=os.path.join(OUTPUT_DIR, "airflow-platform"),
    show=False,
    direction="LR",
    outformat="png",
    graph_attr={
        "bgcolor": "transparent",
        "pad": "0.5",
        "fontcolor": "#e6edf3",
    },
    node_attr={"fontcolor": "#e6edf3"},
    edge_attr={"color": "#4ade80", "fontcolor": "#8b949e"},
):
    mysql = RDS("MySQL\nService DB")

    with Cluster("EC2 (c7i)", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        airflow = Airflow("Airflow\n478 DAGs")

    with Cluster("Storage", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        s3_data = S3("S3\nData Lake")
        s3_log = S3("S3\nLogs")

    catalog = GlueDataCatalog("Glue\nData Catalog")
    athena = Athena("Athena")
    redash = Tableau("Redash")
    users = User("전사 사용자")

    mysql >> Edge(label="추출·가공") >> airflow >> s3_data
    airflow >> Edge(label="로그", style="dashed") >> s3_log

    s3_data >> catalog >> athena >> redash >> users
