// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Records {
    struct RecordItem {
        uint256 timestamp;
        string userId;
        string adminId;
    }

    RecordItem[] public recordList;

    event ItemAdded(uint256 indexed timestamp, string indexed userId, string indexed adminId);

    // constructor() {
    //     owner = msg.sender;
    // }

    function addItem(string memory _userId, string memory _adminId) external  {
        uint256 timestamp = block.timestamp; // Current time

        RecordItem memory newItem = RecordItem(timestamp, _userId, _adminId);
        recordList.push(newItem);

        emit ItemAdded(timestamp, _userId, _adminId);
    }

    function getAllRecordItems() external view returns (RecordItem[] memory) {
        RecordItem[] memory userItems = new RecordItem[](recordList.length);
        uint256 counter = 0;

        for (uint256 i = 0; i < recordList.length; i++) {
            // if (msg.sender == owner) {
                userItems[counter] = recordList[i];
                counter++;
            // }
        }

        // Create a new array with only the relevant items
        RecordItem[] memory result = new RecordItem[](counter);
        for (uint256 j = 0; j < counter; j++) {
            result[j] = userItems[j];
        }

        return result;
    }

    
}
