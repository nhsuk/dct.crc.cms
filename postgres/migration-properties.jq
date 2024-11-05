{
  "properties": {
    "SourceDbServerResourceId": $sourceDbServerResourceId,
    "SecretParameters": {
      "AdminCredentials": {
        "SourceServerPassword": $singleServerAdminPassword,
        "TargetServerPassword": $postgresqlAdminPassword
      }
    },
    "DbsToMigrate": [
      $database
    ],
    "OverwriteDbsInTarget": "True",
    "SslMode": "VerifyFull",
    "SourceType": "PostgreSQLSingleServer"
  }
}
