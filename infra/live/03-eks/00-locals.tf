locals {
    cluster_vpc = {
        id = data.terraform_remote_state.vpc.outputs.vpc_id
        private_subnets_ids = data.terraform_remote_state.vpc.outputs.private_subnets_ids
    }

    eks_cluster = {
        cluster_name = "jarvis"
        cluster_version = "1.27"
        eks_admin_role_name = "AWSReservedSSO_AdministratorAccess_2d5e50f63c106c22"
        initial_node_group_name = "initial_node_group"
    }

    region = var.region

}