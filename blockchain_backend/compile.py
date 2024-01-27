from solcx import compile_standard, install_solc
import json
with open("./recordsContracts.sol","r") as file:
    recordsStorage=file.read()
_solc_version = "0.8.22"
install_solc(_solc_version)
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": recordsStorage}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version=_solc_version,
)
# print(compiled_sol)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["abi"]
bytecode=compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["evm"]["bytecode"]["object"]
with open("abi.json","w") as file:
    json.dump(abi,file)
with open("bytecode.json","w") as file:
    json.dump(bytecode,file)
# print(abi)
print(type(bytecode))
# print(bytecode)