from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, json, os, time, random, pytz

wib = pytz.timezone('Asia/Jakarta')

class NodeWars:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'nodewars.nodepay.ai',
            'Origin': 'https://minigame-nw.nodepay.ai',
            'Pragma': 'no-cache',
            'Referer': 'https://minigame-nw.nodepay.ai/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Node Wars - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def generate_action_logs(self) -> list:
        action_logs = []
        current_timestamp = int(time.time() * 1000000)
        
        possible_prefixes = ['10', '31', '53', '43', '10', '10', '10']
        
        for _ in range(24):
            prefix = random.choice(possible_prefixes)
            unique_number = random.randint(1000, 9999)
            current_timestamp += random.randint(100, 1000)
            action_log = f"{prefix}{unique_number}{current_timestamp}"
            action_logs.append(action_log)
        
        return action_logs

    def generate_random_tokens(self, token_lists: list):
        return {token: random.randint(1, 3) for token in token_lists}
    
    async def user_login(self, query: str, retries=5):
        url = 'https://nodewars.nodepay.ai/auth/login'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': '0',
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['sessionId']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def user_profile(self, query: str, retries=5):
        url = 'https://nodewars.nodepay.ai/users/profile'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def daily_checkin(self, query: str, session_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions/daily'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def do_checkin(self, query: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions/daily/do'
        data = json.dumps({"actionCode":"checkin"})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None
                        
                        response.raise_for_status()
                        result = await response.json()
                        return result['code']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def claim_checkin(self, query: str, session_id: str, mission_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions/daily/claim'
        data = json.dumps({"missionId":mission_id})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None
                        
                        response.raise_for_status()
                        result = await response.json()
                        return result['code']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def user_gifts(self, query: str, session_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/users/gifts'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['gifts']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def receive_gifts(self, query: str, session_id: str, gift_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/users/gifts/receive'
        data = json.dumps({"giftIds":[gift_id]})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['results']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def mission_lists(self, query: str, session_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']['items']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def do_mission(self, query: str, session_id: str, mission_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions/do'
        data = json.dumps({"missionId":mission_id})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
    
    async def claim_mission(self, query: str, session_id: str, mission_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/missions/claim'
        data = json.dumps({"missionId":mission_id})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        if response.status == 400:
                            return None

                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None

    async def claim_nodepay_point(self, query: str, session_id: str, retries=5):
        url = 'https://nodewars.nodepay.ai/users/nodepay/claim'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def start_game(self, query: str, session_id: str, level: int, retries=5):
        url = 'https://nodewars.nodepay.ai/game/start'
        data = json.dumps({'level':level})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def finish_game(self, query: str, session_id: str, action_logs: list, collected_tokens: list, log_id: str, score: int, game_id: str, time_spent: int, retries=5):
        url = 'https://nodewars.nodepay.ai/game/finish'
        data = json.dumps({'actionLogs':action_logs, 'collectedTokens':collected_tokens, 'gameLogId':log_id, 'isCompleted':True, 'score':score, 'sessionId':game_id, 'timeSpent':time_spent})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {query}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['data']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(3)
                else:
                    return None
                
    async def process_query(self, query: str):
        session_id = await self.user_login(query)
        if not session_id:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Query Id Isn't Valid {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if session_id:
            user = await self.user_profile(query)
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['name']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['availablePoints']} Nodepay Points {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['coins']} War Coins {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                await asyncio.sleep(1)

                await self.do_checkin(query)

                check_in = await self.daily_checkin(query, session_id)
                if check_in:
                    is_claimed = check_in.get("isClaimedToday", None)

                    if not is_claimed:
                        new_day = next((item for item in check_in["items"] if item["status"] == "new"), None)
                        if new_day:
                            mission_id = new_day["id"]
                            claim = await self.claim_checkin(query, session_id, mission_id)
                            if claim and claim == "success":
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} Day {check_in['streakDays']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {new_day['reward']} War Coins {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} Day {check_in['streakDays']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} Day {check_in['streakDays']} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Is Already Claimed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                user_gifts = await self.user_gifts(query, session_id)
                if user_gifts:
                    completed = False
                    for gift in user_gifts:
                        gift_id = gift['id']
                        is_claimed = gift['isClaimed']
                        is_expired = gift['isExpired']

                        if gift and not is_expired and not is_claimed:
                            receive = await self.receive_gifts(query, session_id, gift_id)
                            if receive:
                                reward_type = 'Nodepay Points' if gift['giftType'] == 'point' else 'War Coins'
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {gift_id} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {gift['giftAmount']} {reward_type} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} ID {gift_id} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Complete to Claim All Reward {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} No Available Reward {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                mission_lists = await self.mission_lists(query, session_id)
                if mission_lists:
                    completed = False
                    for mission in mission_lists:
                        mission_id = mission['id']
                        reward_type = 'Nodepay Points' if mission['rewardType'] == 'point' else 'War Coins'
                        status = mission['status']

                        if mission and status == 'new':
                            do = await self.do_mission(query, session_id, mission_id)
                            if do:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                                claim = await self.claim_mission(query, session_id, mission_id)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {mission['reward']} {reward_type} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                await asyncio.sleep(1)

                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                        elif mission and status == 'completed':
                            claim = await self.claim_mission(query, session_id, mission_id)
                            if claim:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {mission['reward']} {reward_type} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {mission['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(1)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Mission{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                user = await self.user_profile(query)
                nodepay_point = user['availablePoints']
                if user and nodepay_point >= 100:
                    while True:
                        if nodepay_point < 100:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Nodepay{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} No Available Points to Claim {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                            break

                        claim = await self.claim_nodepay_point(query, session_id)
                        if claim:
                            nodepay_point -= 100
                            claimable = claim['claimedPoint']
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Nodepay{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {claimable} Points {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Nodepay{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        await asyncio.sleep(1)
                        
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Nodepay{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} No Available Points to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                await asyncio.sleep(1)

                level = user['level']
                if level < 101:
                    while level < 101:
                        start = await self.start_game(query, session_id, level)
                        if start:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}                           "
                            )
                            
                            token_lists = [
                                "nodewars", "shiba", "nodepay", "pepe", "polkadot", 
                                "babydoge", "bnb", "avax", "eth", "usdt", "solana", 
                                "aptos", "ton", "bonk", "bomb", "doge", "floki", 
                                "chainlink", "uniswap", "trx", "lido", "xrp", "ltc", 
                                "ada", "sui", "dogwifhat", "near", "bitcoin"
                            ]
                            
                            action_logs = self.generate_action_logs()
                            collected_tokens = self.generate_random_tokens(token_lists)
                            game_id = start['sessionId']
                            score = start['gameConfigByLevel']['requiredScore']
                            log_id = start['gameLogId']
                            time_spent = random.randint(25000, 30000)

                            delay = random.randint(5, 10)
                            for remaining in range(delay, 0, -1):
                                print(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}Seconds to Finish Game{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                                    end="\r",
                                    flush=True
                                )
                                await asyncio.sleep(1)

                            finish = await self.finish_game(query, session_id, action_logs, collected_tokens, log_id, score, game_id, time_spent)
                            if finish:
                                level_up = finish['isLevelUp']
                                if level_up:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Finished{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Status{Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT} Level UP {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Is Finished{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} ] [ Status{Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT} Not Level UP {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Finished{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}          "
                                )

                            level += 1

                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} Level {level} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}           "
                            )
                            break

                        delay = random.randint(15, 20)
                        for remaining in range(delay, 0, -1):
                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}Seconds to Start Next Game{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                                end="\r",
                                flush=True
                            )
                            await asyncio.sleep(1)

                    if level == 101:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Reached Max Level {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                          "
                        )

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Game{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Reached Max Level {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )

    async def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        await self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        await asyncio.sleep(3)
                        

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'query.txt' tidak ditemukan.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = NodeWars()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Node Wars - BOT{Style.RESET_ALL}",                                       
        )