#!/usr/bin/python
import asyncio
import datetime
import sys
from random import choice, randint
import gc
import typing

from decouple import config
from playwright.async_api import Playwright, TimeoutError, async_playwright

sys.setrecursionlimit(1048 * 4)
SITEGOOGLE = config('SITEGOOGLE')
SITEADD = config('SITEADD')
SITETWITTER = config('SITETWITTER')
SITEINSTAGRAM = config('SITEINSTAGRAM')
SITEDISCORD = config('SITEDISCORD')

EMAILGOOGLE = config('EMAILGOOGLE')
EMAILADD = config('EMAILADD')
EMAILTWITTER = config('EMAILTWITTER')
EMAILINSTAGRAM = config('EMAILINSTAGRAM')
EMAILDISCORD = config('EMAILDISCORD')

PASSWORDGOOGLE = config('PASSWORDGOOGLE')
PASSWORDADD = config('PASSWORDADD')
PASSWORDTWITTER = config('PASSWORDTWITTER')
PASSWORDINSTAGRAM = config('PASSWORDINSTAGRAM')
PASSWORDDISCORD = config('PASSWORDDISCORD')

NoneType = type(None)


class MyBrowser(object):
    def __init__(self) -> NoneType:
        self.page1 = None
        self.page_popup = None
        self.page = None
        self.context = None
        self.browser = None
        self.name = None
        self.contadorjust = 0
        self.contador1 = 0
        self.contador = 0
        self.titulo = str
        self.lista_titulos = [
            'AddMeFast.com - FREE Social Media Marketing & Crypto Promotion',  # 0
            'AddMeFast.com - Login',  # 1
            'AddMeFast.com - Welcome',  # 2
            'Just a moment...',  # 3
            'AddMeFast.com - YouTube Subscribe',  # 4
            'AddMeFast.com - YouTube Likes',  # 5
            'AddMeFast.com - Twitter Likes',  # 6
            'AddMeFast.com - Twitter Retweets',  # 7
            'AddMeFast.com - Twitter Followers',  # 8
            'AddMeFast.com - Instagram Likes',  # 9
            'AddMeFast.com - Instagram Followers',  # 10
            'AddMeFast.com - Discord Members',  # 11
            'AddMeFast.com - Reddit Community Members',  # 12
            'AddMeFast.com - Reddit post and comment upvotes',  # 13
            'Attention Required! | Cloudflare',  # 14
        ]
        self.SITE_MAP = {
            'ELEMENTS': {
                'GOOGLE': {
                    'EMAIL': 'css=#identifierId',
                    'AVANÇAR': 'role=button[name="Next"]',
                    'PASSWORD': '#password .whsOnd',
                },
                'TWITTER': {
                    'EMAIL': 'input[name="text"]',
                    'PASSWORD': 'input[name="password"]',
                },
                'INSTAGRAM': {
                    'EMAIL': '[aria-label="Phone number, username, or email"]',
                    'PASSWORD': 'input[name="password"]',
                },
                'DISCORD': {
                    'EMAIL': 'text="Email or Phone Number"',
                    'PASSWORD': 'text="Password"',
                },
                'REDDIT': {
                    'EMAIL': 'text=Continue with Google',
                    'PASSWORD': '',
                },
                'ADDMEFAST': {'EMAIL': 'Email', 'PASSWORD': 'Password'},
                'GUIAS': {
                    'TWITTER-LIKES': 'Twitter Likes',
                    'TWITTER-FOLLOWERS': 'Twitter Followers',
                    'TWITTER-RETWEETS': 'Twitter Retweets',
                    'DISCORD-MEMBERS': 'Discord Members',
                    'REDDIT-MEMBERS': 'Reddit Members',
                    'REDDIT-UPVOTES': 'Reddit Upvotes',
                    'INSTAGRAM-FOLLOWERS': 'Instagram FollowersHigh CPC Rates (many active links)',
                    'INSTAGRAM-LIKES': 'Instagram Likes',
                    'YOUTUBE-LIKES': 'YouTube Likes',
                    'YOUTUBE-SUBSCRIBE': 'YouTube Subscribe',
                    'BONUS': 'Daily Bonus',
                },
                'POPUPS': {
                    'FOLLOW': '#form1 a:has-text("Follow")',
                    'RETWEET': '#form1 a:has-text("Retweet")',
                    'LIKE': '#form1 a:has-text("Like")',
                    'JOIN': '#form1 a:has-text("Join")',
                    'SHARE': '#form1 a:has-text("Share")',
                    'UPVOTE': '#form1 a:has-text("Upvote")',
                    'SUBSCRIBE': '#form1 a:has-text("Subscribe")',
                },
                'ELEMENT-FINAL': {
                    'YOUTUBE-SUBSCRIBE': 'css=.yt-spec-touch-feedback-shape--touch-response-inverse > '
                                         '.yt-spec-touch-feedback-shape__fill',
                    'YOUTUBE-LIKE': '#segmented-like-button > ytd-toggle-button-renderer > yt-button-shape > button > '
                                    'yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill',
                    'TWITTER': 'xpath=//span/span',
                    'INSTAGRAM-LIKE': '._aamw > ._abl-',
                    'INSTAGRAM-FOLLOW': 'xpath=//button/div/div',
                    'DISCORD-MEMBER': "xpath=//button[contains(.,'Aceitar convite')]",
                    'REDDIT-UPVOTE': 'xpath=//div[2]/div/div/div/div/button/span/i',
                },
            }
        }

    async def FuncBrowser(self, playwright: typing.Optional[Playwright], name: typing.Optional[str]):
        """
        Armazena o browser name na variavel self.browser,
        e retorna o self.browser para a proximas iterações.
        """
        self.name = name
        if self.name == 'firefox':
            self.browser = await playwright.firefox.launch_persistent_context(
                headless=True, user_data_dir=r'firefox', slow_mo=50
            )
        elif self.name == 'chromium':
            self.browser = await playwright.chromium.launch(headless=False, channel="msedge")
        elif self.name == 'webkit':
            self.browser = await playwright.webkit.launch(headless=False)
        # self.context = await self.browser.new_context()
        self.page = await self.browser.new_page()
        await asyncio.sleep(1)
        await self.browser.pages[0].close()
        return self.page

    async def close(self):
        return await self.browser.close()

    async def site(self, url):
        return await self.page.goto(url)

    async def title(self):
        result = await self.page.title()
        return result

    async def elemento_visivel(self, element) -> bool:
        elemento_visivel = self.page.locator(element).nth(0)
        return await elemento_visivel.is_visible()

    async def popup_visivel(self, element) -> bool:
        elemento_visivel = self.page_popup.locator(element).nth(0)
        return await elemento_visivel.is_visible()

    async def escreva_no_elemento(self, element, escreva):
        try:
            result = self.page.locator(element)
            return await result.fill(escreva)
        except TimeoutError:
            print(f'Acabaram os Popups: \n• Element: {element}')

    async def enter(self, element, escreva):
        try:
            result = self.page.locator(element)
            return await result.press(escreva)
        except TimeoutError:
            print(f'Timeout Error: \n• Element: {element}')

    async def ForceClick(self, element):
        try:
            box = await self.page.wait_for_selector(element)
            box = await box.bounding_box()
            await self.page.mouse.click(
                box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
            )
        except TimeoutError:
            print(f'Timeout Error: \n• Element: {element}')

    async def LoginAddmeFasT(self):
        try:
            await asyncio.sleep(1)
            await self.page.get_by_placeholder(
                self.SITE_MAP['ELEMENTS']['ADDMEFAST']['EMAIL']
            ).fill(EMAILADD)
            await self.page.get_by_placeholder(
                self.SITE_MAP['ELEMENTS']['ADDMEFAST']['PASSWORD']
            ).fill(PASSWORDADD)
            await self.page.get_by_role('button', name='Login').click()
            await self.page.wait_for_url('https://addmefast.com/welcome')
            await self.page.wait_for_timeout(5000)
        except TimeoutError:
            pass

    async def check_all_title(self):
        gc.collect()
        """
        Checa o self.titulo da pagina atual e faz comparações
        com título ja correspondentes de locais predeterminados
        para movimentação entre paginas dentro do site
        """
        #  self.page.set_default_timeout(10000)
        for self.titulo in self.lista_titulos:
            if self.titulo == await self.title() and await self.title() == self.lista_titulos[0]:
                await self.LoginAddmeFasT()
                return await self.check_all_title()
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[1]:
                await self.LoginAddmeFasT()
                return await self.check_all_title()
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[2]:
                return await self.menu()
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[3]:
                self.contadorjust = self.contadorjust+1
                if self.contadorjust == 3:
                    await self.close()
                    return main()
                await asyncio.sleep(30)
                return await self.check_all_title()
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[4]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL'][
                        'YOUTUBE-SUBSCRIBE'
                    ]
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[5]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['YOUTUBE-LIKE']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[6]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['TWITTER']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[7]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['TWITTER']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[8]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['TWITTER']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[9]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL'][
                        'INSTAGRAM-LIKE'
                    ]
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[10]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL'][
                        'INSTAGRAM-FOLLOW'
                    ]
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[11]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL'][
                        'DISCORD-MEMBER'
                    ]
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[12]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[13]:
                return await self.finalizando_popups(
                    self.SITE_MAP['ELEMENTS']['ELEMENT-FINAL']['REDDIT-UPVOTE']
                )
            elif self.titulo == await self.title() and await self.title() == self.lista_titulos[14]:
                await self.close()

    async def popups(self, element_popup):
        gc.collect()
        try:
            datetime.datetime.now().strftime('%H:%M')
            print(datetime.datetime.now().strftime('%H:%M'))
            if (
                    datetime.datetime.now().strftime('%H:%M') == '20:50'
                    or datetime.datetime.now().strftime('%H:%M') == '20:51'
                    or datetime.datetime.now().strftime('%H:%M') == '20:52'
                    or datetime.datetime.now().strftime('%H:%M') == '20:53'
                    or datetime.datetime.now().strftime('%H:%M') == '20:54'
                    or datetime.datetime.now().strftime('%H:%M') == '20:55'
            ):
                print('VERDADE')
                # return await self.guias('YOUTUBE-LIKES')
            # await self.page.wait_for_selector(".fs18")
            points = await self.page.locator(
                '//*[@id="toppointsbalance"]'
            ).all_inner_texts()

            element1 = False
            while not element1:
                self.contador1 = self.contador1 + 1
                await asyncio.sleep(1)
                fs18 = await self.page.locator('.fs18').all_inner_texts()
                if await self.page.locator('.fs18').all_inner_texts() == [
                    'No items in this network for now. Please try later.'
                ]:
                    print('Acabaram os Popups Nessa Guia !')
                    element1 = True
                    return await self.menu()
                elif (
                        fs18
                        != ['No items in this network for now. Please try later.']
                        and fs18 != []
                ):
                    element1 = True
                elif self.contador1 == 20:
                    element1 = True
            print(f'Total Points: {points}')
            await asyncio.sleep(2)
            async with self.page.expect_popup() as popup_info:
                await self.page.locator(element_popup).click()
            return await popup_info.value
        except TimeoutError:
            print(f'Timeout Error: \n• Element: {element_popup}')
            return await self.menu()

    async def finalizando_popups(self, element_final):
        self.page_popup = await self.popups('css=.btn3')
        element = False
        while not element:
            self.contador = self.contador + 1
            await asyncio.sleep(1)
            if await self.popup_visivel(element_final):
                await self.page_popup.wait_for_timeout(randint(250, 500))
                await self.page_popup.locator(element_final).nth(0).click()
                print('Popup finalizado com sucesso')
                element = True
            elif self.contador == 20:
                print('Popup não finalizado')
                element = True
        gc.collect()
        if not self.page_popup.is_closed():
            await self.page_popup.wait_for_timeout(randint(2000, 4000))
            await self.page_popup.close()
            await asyncio.sleep(1)
            confirm = await self.elemento_visivel('a:has-text("Confirm")')
            if confirm:
                await self.page.locator(
                    'css=.btn3', has_text='Confirm'
                ).click()
                await asyncio.sleep(1)
                return await self.finalizando_popups(element_final)
            else:
                await asyncio.sleep(1)
                return await self.finalizando_popups(element_final)
        else:
            await asyncio.sleep(1)
            return await self.check_all_title()

    async def menu(self) -> int:
        print('Bem-vindo ao Menu Principal')
        m = (0, 1, 2, 3, 4, 5, 7, 8, 9)  # até 9
        m = choice(tuple(m))
        if m == 0:
            return await self.guias('TWITTER-LIKES')  # 0
        elif m == 1:
            return await self.guias('TWITTER-RETWEETS')  # 1
        elif m == 2:
            return await self.guias('TWITTER-FOLLOWERS')  # 2
        elif m == 3:
            return await self.guias('INSTAGRAM-LIKES')  # 3
        elif m == 4:
            return await self.guias('INSTAGRAM-FOLLOWERS')  # 4
        elif m == 5:
            return await self.guias('DISCORD-MEMBERS')  # 5
        elif m == 6:
            return await self.guias('REDDIT-MEMBERS')  # 6
        elif m == 7:
            return await self.guias('REDDIT-UPVOTES')  # 7
        elif m == 8:
            return await self.guias('YOUTUBE-SUBSCRIBE')  # 8
        elif m == 9:
            return await self.guias('YOUTUBE-LIKES')  # 9

    async def guias(self, element):
        gc.collect()
        await self.page.get_by_role(
            'link', name=self.SITE_MAP['ELEMENTS']['GUIAS'][element]
        ).click()
        print(await self.title())
        return await self.check_all_title()

    async def loginadde(self):
        try:
            await self.page.goto(SITEADD, wait_until='load')
            await asyncio.sleep(1)
            await self.page.locator('[placeholder="Email"]').fill(EMAILADD)
            await asyncio.sleep(1)
            await self.page.locator('[placeholder="Email"]').press('Tab')
            await asyncio.sleep(1)
            await self.page.locator('[placeholder="Password"]').fill(
                PASSWORDADD
            )
            await asyncio.sleep(1)
            await self.page.locator('[placeholder="Password"]').press('Enter')
            await asyncio.sleep(1)
            await self.page.wait_for_url(
                'https://addmefast.com/welcome', wait_until='load'
            )
            await self.page.wait_for_timeout(3000)
            print('Logado')
            return '• feito login'
        except:
            await asyncio.sleep(1)
            print(await self.title())
            return await self.loginadde()

    async def logingoogle(self):
        try:
            self.page.set_default_timeout(10000)
            await self.page.goto(SITEGOOGLE, wait_until='load')
            await asyncio.sleep(3)
            if await self.page.title() == 'Conta do Google':
                print('Logado')
                return None
            if (
                    self.page.url
                    == 'https://myaccount.google.com/?utm_source=sign_in_no_continue&pli=1'
            ):
                print('Logado')
                return None
            await self.page.locator('css=#identifierId').fill(EMAILGOOGLE)
            await asyncio.sleep(1)
            await self.page.locator('css=#identifierId').press('Enter')
            await asyncio.sleep(1)
            await self.page.wait_for_load_state('load')
            await asyncio.sleep(1)
            await self.page.locator('css=#password .whsOnd').fill(
                PASSWORDGOOGLE
            )
            await asyncio.sleep(1)
            await self.page.locator('css=#password .whsOnd').press('Enter')
            await asyncio.sleep(1)
            await self.page.wait_for_load_state('load')
            await self.page.wait_for_timeout(5000)
            print('Logado')
            return '• feito login'
        except:
            print(await self.title())
            await asyncio.sleep(1)
            return await self.logingoogle()

    async def logintwitter(self):
        try:
            await self.page.goto(SITETWITTER, wait_until='load')
            await asyncio.sleep(1)
            await self.page.locator('input[name="text"]').fill(EMAILTWITTER)
            await asyncio.sleep(1)
            await self.page.locator('input[name="text"]').press('Enter')
            await asyncio.sleep(1)
            await self.page.wait_for_load_state('load')
            await asyncio.sleep(1)
            await self.page.locator('input[name="password"]').fill(
                PASSWORDTWITTER
            )
            await asyncio.sleep(1)
            await self.page.locator('input[name="password"]').press('Enter')
            await asyncio.sleep(2)
            if await self.page.title() == '(4) Log in to Twitter / Twitter':
                print('Logado')
                return None
            await self.page.wait_for_timeout(5000)
            print('Logado')
            return 'feito login'
        except:
            print(await self.title())
            await asyncio.sleep(1)
            return await self.logintwitter()

    async def logininsta(self):
        try:
            await self.page.goto(SITEINSTAGRAM, wait_until='load')
            await asyncio.sleep(3)
            if not await self.elemento_visivel('input[name="username"]'):
                print('Logado')
                return None
            await self.page.locator('input[name="username"]').fill(
                EMAILINSTAGRAM
            )
            await asyncio.sleep(1)
            await self.page.locator('input[name="username"]').press('Tab')
            await asyncio.sleep(1)
            await self.page.locator('input[name="password"]').fill(
                PASSWORDINSTAGRAM
            )
            await self.page.locator('input[name="password"]').press('Enter')
            await self.page.wait_for_timeout(10000)
            print('Logado')
            return 'feito login'
        except:
            print(await self.title())
            await asyncio.sleep(1)
            return await self.logininsta()

    async def logindiscord(self):
        try:
            await self.page.goto(SITEDISCORD)
            await asyncio.sleep(3)
            if self.page.url == 'https://discord.com/channels/@me':
                print('Logado')
                return None
            if await self.page.title() == "Discord":
                print('Logado')
                return None
            else:
                await self.page.locator('#uid_5').fill(
                    EMAILDISCORD
                )
                await asyncio.sleep(1)
                await self.page.locator('#uid_5').press(
                    'Tab'
                )
                await asyncio.sleep(1)
                await self.page.locator('#uid_8').fill(PASSWORDDISCORD)
                await asyncio.sleep(1)
                await self.page.locator('#uid_8').press('Enter')
                await asyncio.sleep(1)
                await self.page.wait_for_timeout(10000)
                print('Logado')
                return 'feito login'
        except:
            print(await self.title())
            await asyncio.sleep(1)
            return await self.logindiscord()

    async def loginreddit(self):
        try:
            await self.page.goto('https://www.reddit.com/login/')
            await asyncio.sleep(2)
            if await self.page.title() == 'reddit.com: Welcome back':
                print('Logado')
                return None
            else:
                await self.page.locator('css=#loginUsername').fill("Sure_Driver_4287")
                await asyncio.sleep(1)
                await self.page.locator('css=#loginPassword').fill("2406379431")
                await asyncio.sleep(1)
                await self.page.locator('css=#loginPassword').press('Enter')
                await asyncio.sleep(1)
                await self.page.wait_for_load_state('load')
                await self.page.wait_for_timeout(5000)
                print('Logado')
                return 'feito login'
        except:
            print(await self.title())
            await asyncio.sleep(1)
            return await self.loginreddit()

    async def alllogin(self):
        await self.logingoogle()
        await self.logininsta()
        await self.logindiscord()
        await self.loginreddit()
        await self.logintwitter()
        await self.site(SITEADD)
        return await self.check_all_title()


async def main():
    try:
        browser = MyBrowser()
        async with async_playwright() as playwright:
            await browser.FuncBrowser(playwright, 'firefox')
            await browser.alllogin()
    except TimeoutError as tm:
        print(tm)
    except Exception as e:
        print(e)
    finally:
        gc.collect()
        gc.enable()
        # return await main()


if __name__ == '__main__':
    while True:
        asyncio.run(main())
        continue
