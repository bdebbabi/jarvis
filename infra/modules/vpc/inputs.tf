variable "vpc" {
  type = object({
    name = string
    vpc_cidr = string
    azs = list(string)
    public_subnet_cidrs = list(string)
    private_subnet_cidrs = list(string)
  })
}
