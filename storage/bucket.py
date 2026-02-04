from botocore.exceptions import ClientError


class Bucket:
    def __init__(self, name, client, **options):
        self._name = name
        self._client = client
        self._options = options
        self._existed = False

    @property
    def existed(self):
        return self._existed

    def create(self):
        try:
            response = self._client.create_bucket(Bucket=self._name)
            return response
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")

            if error_code == "BucketAlreadyOwnedByYou":
                self._existed = True
                print("Bucket already exists and is owned by you")
            else:
                raise

    def set_lifecycle(
        self,
        policy_name: str,
        expiration_days: int,
        noncurrent_expiration_days: int | None = None,
    ) -> None:
        lifecycle_config = {
            "Rules": [
                {
                    "ID": policy_name,
                    "Prefix": "",
                    "Status": "Enabled",
                    "Expiration": {"Days": expiration_days},
                    "Filter": {},
                }
            ]
        }
        if noncurrent_expiration_days:
            lifecycle_config["Rules"][0]["NoncurrentVersionExpiration"] = {
                "NoncurrentDays": noncurrent_expiration_days
            }

        self._client.put_bucket_lifecycle_configuration(
            Bucket=self._name, LifecycleConfiguration=lifecycle_config
        )

    def set_versioning(self, status):
        assert status in ["Enabled", "Suspended"], (
            '"{status}" is an unexpected versioning status. '
        )
        self._client.put_bucket_versioning(
            Bucket=self._name, VersioningConfiguration={"Status": status}
        )
