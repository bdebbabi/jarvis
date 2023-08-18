locals {
    cluster_vpc = {
        name="cluster"
        azs = ["eu-west-3a", "eu-west-3b"]
        vpc_cidr= "10.0.0.0/16" 
        public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
        private_subnet_cidrs = ["10.0.101.0/24", "10.0.102.0/24"]
    }
}