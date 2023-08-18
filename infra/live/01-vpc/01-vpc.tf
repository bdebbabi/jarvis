module "cluster_vpc" {
    source = "../../modules/vpc"  
    vpc = local.cluster_vpc
}