terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

resource "local_file" "note" {
  filename = "${path.module}/onboarding.txt"
  content  = "Welcome Manos to the AI Engineering Team! Project: FastAPI + React + Angular"
}

resource "local_file" "backup_note" {
  filename = "${path.module}/backup.txt"
  content  = "This is a backup of: ${local_file.note.content}"
}
