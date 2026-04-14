"""Airflow 워크플로우 플랫폼 아키텍처 다이어그램.

Airflow 도입(2025.03-2026.01) 프로젝트의
통합 후 아키텍처를 시각화한다.
"""

import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.workflow import Airflow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(BASE_DIR, "..", "images", "aws-icons")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "images")

# 아이콘 경로
IC_RDS = os.path.join(ICONS, "Databases", "Arch_Amazon-RDS_64.png")
IC_EC2 = os.path.join(ICONS, "Compute", "Arch_Amazon-EC2_64.png")
IC_S3 = os.path.join(ICONS, "Storage", "Arch_Amazon-Simple-Storage-Service_64.png")
IC_GLUE = os.path.join(ICONS, "Analytics", "Arch_AWS-Glue_64.png")
IC_ATHENA = os.path.join(ICONS, "Analytics", "Arch_Amazon-Athena_64.png")
IC_REDASH = os.path.join(BASE_DIR, "..", "images", "third-party", "redash.png")

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
    mysql = Custom("MySQL\nService DB", IC_RDS)

    with Cluster("EC2 (c7i)", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        airflow = Airflow("Airflow\n478 DAGs")

    with Cluster("Storage", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        s3_data = Custom("S3\nData Lake", IC_S3)
        s3_log = Custom("S3\nLogs", IC_S3)

    catalog = Custom("Glue\nData Catalog", IC_GLUE)
    athena = Custom("Athena", IC_ATHENA)
    redash = Custom("Redash", IC_REDASH)
    users = User("전사 사용자")

    mysql >> Edge(label="추출·가공") >> airflow >> s3_data
    airflow >> Edge(label="로그", style="dashed") >> s3_log

    s3_data >> catalog >> athena >> redash >> users
