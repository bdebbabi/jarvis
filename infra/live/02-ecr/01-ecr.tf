module "front_ecr" {
    source = "../../modules/ecr"  
    ecr = local.front_ecr
}

module "back_ecr" {
    source = "../../modules/ecr"  
    ecr = local.back_ecr
}