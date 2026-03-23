# 1. Ορίζουμε τον Provider για τοπικά αρχεία
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

# 2. Λέμε στην Terraform να φτιάξει ένα αρχείο κειμένου
resource "local_file" "capco_note" {
  filename = "${path.module}/capco_onboarding.txt"
  content  = "Welcome Manos to the AI Engineering Team! Project: FastAPI + React + Angular"
}

# 3. Λέμε στην Terraform να φτιάξει έναν δεύτερο αρχείο με το όνομα του πρώτου
resource "local_file" "backup_note" {
  filename = "${path.module}/backup.txt"
  content  = "This is a backup of: ${local_file.capco_note.content}"
}