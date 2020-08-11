Reference Count
===============

This is a demo to show how to handle MSI reference count during install & uninstall.

### Sample

```
{
    "ProductCode": "{4A5016E3-C9DD-4595-8A4B-053A7A6335F6}",
    "References": {
        "{13B5D516-1B2F-4999-AC76-D0B4071E2551}": 
        {
            "File": "[{ProgramFilesCommonX64}]\\shared.file",
            "Registry": {
                "HKEY_LOCAL_MACHINE\\SOFTWARE\\Test": [],
                "HKEY_LOCAL_MACHINE\\SOFTWARE\\Test1": [
                    "Test2"
                ]
            }
        }
    }
}
```