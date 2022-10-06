<div align="center">
	<h2>ERPNext Workspace for Pakistan ☪️</h2>
	<img src="https://raw.githubusercontent.com/abid-omar/erpnext_pk/master/erpnext_pk/public/images/erpnext-pk-banner.png">
	</div>

The Pakistan Workspace is a localization app for [ERPNext](https://github.com/frappe/erpnext) that adds regional custom fields for NIC, NTN, and STRN numbers, and reports for FBR tax compliance.

## Features 🎁

### 1. NIC, NTN, and STRN numbers
**Custom fields** are added to the Customer, Supplier and Employee DocTypes with a format input mask and length validation.

- 🪪 **NIC** National Identity Card number (`tax_nic`) 
- 🧾 **NTN** National Tax Number (`tax_ntn`)
- 🧾 **STRN** Sales Tax Registration Number (`tax_strn`)

### 2. Tax accounting and reporting 🏦
**Tax accounts** are added to the Company Master for tax accounting and reporting.

- Sales tax on goods
- Sales tax on services
- Further tax
- Extra tax

**Reports** are automatically created for tax compliant sales invoices. Reports can be exported file for validation and upload to the eFBR IRIS platform.
- DSI Domestic Sales Invoices (Annexure C)
- SRB Sales Tax on Services

### 3. Other Features
- HR Module: Employee NIC numnber, date of issue and date of expiry.

<img src="https://raw.githubusercontent.com/abid-omar/erpnext_pk/master/erpnext_pk/public/images/erpnext-pk-screenshot.png">

## Installation 🧑‍💻
The Pakistan Workspace can be installed via Bench CLI on an active ERPNext site. 

```python
bench get-app https://github.com/ParaLogicTech/erpnext_pk.git
bench --site [site name] install-app erpnext_pk
```

## Roadmap & Wishlist ✨
- Print formats to include NIC, NTN and/or STRN numbers
- Sales tax on services for other provinces
- Witholding tax fields and reporting
- Automatically add PCT/HS codes and description
- Reports and compliance for
	- DPI Domestic Purchase Invoices (Annexure A)
	- GDI Goods Declaration - Imports (Annexure B)
	- GDE Goods Declaration - Exports (Annexure D)
	- Federal Excises (Annexure E)
	- DCN Debit and Credit Notes (Annexure I)

## Support 🤗
Please contact us for any support or other inquiries via our website https://paralogic.io.

## Contributing 🤝
You can fork this repository and create a pull request to contribute code. By contributing to ERPNext Pakistan Workspace, you agree that your contributions will be licensed under its GNU General Public License (v3). 

## GNU/General Public License 
The ERPNext Pakistan Workspace code is licensed as GNU General Public License (v3) and the copyright is owned by ParaLogic and Contributors (see [license.txt](license.txt)).
