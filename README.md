Pakistan Workspace/Module
==========================
name: erpnext_pk

description: ERPNext Workspace/Module for Pakistan, localized with regional custom fields and reports for tax compliance

The Pakistan Workspace is a localization app for ERPNext that adds regional custom fields such as NIC, NTN, and STRN numbers, and reports for FBR tax compliance. The app is available for one-click installation on the Frappe Marketplace, or can be deployed via Bench CLI for self-hosted options.

## Features
### 1. NIC, NTN, and STRN numbers
Custom fields are added to the Customer and Supplier DocTypes with a format input mask and length validation.

NIC National Identity Card number (fieldname:tax_pk_nic)
NTN National Tax Number (fieldname:tax_pk_ntn)
STRN Sales Tax Registration Number (fieldname:tax_pk_strn)

### 2. FBR compliant tax reports
Report: "Sales Tax - DSI Domestic Sales Invoices (Annexure C)"

### 3. Other Features
- Print formats modified to include NIC, NTN and/or STRN as applicable
- Delivery Challan (renamed from Delivery Note)

## Installation Instructions
1. Frappe Marketplace
2. Bench CLI

## Roadmap

## Contributing

## Support
Please contact us for any support or other inquiries via our website.

## License
GNU/General Public License (see [license.txt](license.txt))

The ERPNext Pakistan code is licensed as GNU General Public License (v3) and the copyright is owned by ParaLogic and Contributors.

By contributing to ERPNext Pakistan App, you agree that your contributions will be licensed under its GNU General Public License (v3).
