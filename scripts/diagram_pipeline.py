"""데이터 파이프라인 아키텍처 다이어그램.

데이터 파이프라인 설계·도입(2022.07-2023.03) 프로젝트의
최종 아키텍처를 시각화한다. 4곳에 분산된 인프라 구조를 보여준다.
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import Athena, GlueCrawlers, GlueDataCatalog
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.analytics import Tableau

import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

with Diagram(
    "",
    filename=os.path.join(OUTPUT_DIR, "data-pipeline"),
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

    with Cluster("ETL (4곳 분산)", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        glue = GlueCrawlers("Glue\n대부분 테이블")
        mac = EC2("Mac Studio\n대용량 테이블")
        ec2 = EC2("EC2\n가공 스크립트")

    with Cluster("Storage", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        s3 = S3("S3\nraw / core / output")

    catalog = GlueDataCatalog("Glue\nData Catalog")
    athena = Athena("Athena")
    redash = Tableau("Redash")
    users = User("전사 사용자")

    mysql >> Edge(label="Spark") >> glue >> s3
    mysql >> Edge(label="pandas") >> mac >> s3
    mysql >> Edge(label="Python") >> ec2 >> s3

    s3 >> catalog >> athena >> redash >> users
