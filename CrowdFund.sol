// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IERC20 {
    function transfer(address, uint) external returns (bool);

    function transferFrom(
        address,
        address,
        uint
    ) external returns (bool);
}

contract CrowdFund {

    event Launch (
        uint256 id,
        address indexed creator, // indexed so we can find all campaigns lauched by the same creator
        uint goal,
        uint32 startAt,
        uint32 endAt
    );
    event Cancel(uint256 id);
    event Pledge(uint256 indexed id, address indexed caller, uint amount);
    event Unpledge(uint256 indexed id, address indexed caller, uint amount);
    event Claim(uint256 id);
    event Refund(uint256 indexed id, address indexed caller, uint amount);

    struct Campaign {
        address creator;
        uint256 goal;
        uint256 pledged;
        uint32 startAt;
        uint32 endAt;
        bool claimed;
    }

    // We only support 1 token per contract 
    //in order to prevent risks in case 1 token has vulnerabilities
    IERC20 public immutable token;

    // count -> total campaigns created and generates id for new campaign
    uint public count;

    // mapping id to campaign
    mapping(uint256 =>Campaign) public campaigns;
    mapping(uint256 => mapping(address => uint256)) public pledgedAmount;

    constructor(address _token) {
        token = IERC20(_token);
    }         

    function launch(
        uint _goal,
        uint32 _startAt,
        uint32 _endAt
    ) external {
        require(_startAt >= block.timestamp, "start at < now");
        require(_endAt >= _startAt, "end at < start at");
        require(_endAt <= block.timestamp + 90 days, "end at > max duration");
    
        count += 1;
        campaigns[count] = Campaign({
            creator: msg.sender,
            goal: _goal,
            pledged: 0,
            startAt: _startAt,
            endAt: _endAt,
            claimed: false
        });

        emit Launch(count, msg.sender, _goal, _startAt, _endAt);
    }


    function cancel(uint _id) external {
        Campaign memory campaign = campaigns[_id];
        require(msg.sender == campaign.creator, "not creator");
        require(block.timestamp < campaign.startAt, "started");
        delete campaigns[_id];
        emit Cancel(_id);
    }

    function pledge(uint _id, uint _amount) external {
        // declare campaign as storage because we will update it
        Campaign storage campaign = campaigns[_id];
        require(block.timestamp >= campaign.startAt, "campaign not started");
        require(block.timestamp <= campaign.endAt, "campaign ended");

        campaign.pledged += _amount;
        pledgedAmount[_id][msg.sender] += _amount;
        token.transferFrom(msg.sender, address(this), _amount);

        emit Pledge(_id, msg.sender, _amount);        
    }

    function unpledge(uint _id, uint _amount) external {
        // declare campaign as storage because we will update it
        Campaign storage campaign = campaigns[_id];
        require(block.timestamp <= campaign.endAt, "campaign ended");
        
        campaign.pledged -= _amount;
        pledgedAmount[_id][msg.sender] -= _amount;
        token.transfer(msg.sender, _amount);

        emit Unpledge(_id, msg.sender, _amount);
    }

    function claim(uint _id) external {
        Campaign storage campaign = campaigns[_id];
        require(msg.sender == campaign.creator, "Only creator can claim");
        require(block.timestamp > campaign.endAt, "campaign not ended");
        require(campaign.pledged >= campaign.goal, "pledged < goal");
        require(!campaign.claimed, "claimed");

        campaign.claimed = true;
        // accessing msg.sender is cheaper than accessing campaign.creator
        token.transfer(msg.sender, campaign.pledged);

        emit Claim(_id);
    }

    function refund(uint _id) external {
        Campaign storage campaign = campaigns[_id];
        require(msg.sender == campaign.creator, "Only creator can claim");
        require(block.timestamp > campaign.endAt, "campaign not ended");
        require(campaign.pledged < campaign.goal, "pledged < goal");
 
        uint256 bal = pledgedAmount[_id][msg.sender];
        // reset ballance to prevent reentrancy effect
        pledgedAmount[_id][msg.sender] = 0;
        token.transfer(msg.sender, bal);
        emit Refund(_id, msg.sender, bal);
    }
}
