module "eks_cluster" {
    source = "../../modules/eks"  
    vpc = local.cluster_vpc
    eks = local.eks_cluster
    region = local.region
}