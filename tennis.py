import pygame
import random

#Pygame Hazırlık
pygame.init()

#pencere ayarları
GENISLIK,YUKSEKLIK=1200,750
pencere=pygame.display.set_mode((GENISLIK,YUKSEKLIK))

#FPS İşlemleri
FPS=30
saat=pygame.time.Clock()

#Sınıflar
class Oyun():
    def __init__(self,oyuncu1,oyuncu2,top_grup):
        #Parametre Değişkenleri
        self.oyuncu1=oyuncu1
        self.oyuncu2=oyuncu2
        self.top_grup=top_grup
        #Arka Plan Görüntüsü ve Bitti Görüntüsü
        self.arka_plan=pygame.image.load('arka_plan.jpg')
        self.oyun_bitti=pygame.image.load('oyun_bitti.jpg')
        #Oyun Değişkenleri
        self.oyuncu1_puan=0
        self.oyuncu2_puan=0
        self.puan=5
        self.sayac=30
        self.fps_say=0
        #Oyun Font
        self.oyun_font=pygame.font.Font('oyun_font.ttf',40)
        #Şarkı ve ses Efektleri
        self.kenar_ses=pygame.mixer.Sound('puan_gitti.wav')
        self.carpisma_sesi=pygame.mixer.Sound('temas.wav')
        pygame.mixer.music.load('oyun_sarki.wav')
        pygame.mixer.music.play(-1)
    def update(self):
        self.fps_say+=1
        if self.fps_say==FPS:
            self.sayac-=1
            self.fps_say=0
            if self.sayac==0:
                self.bitir()

        self.temas()
        self.oyun_durum()
    def cizdir(self):
        pencere.blit(self.arka_plan,(0,0))

        puan1=self.oyun_font.render('1. Player Score:'+str(self.oyuncu1_puan),True,(0,50,150))
        puan1_konum=puan1.get_rect()
        puan1_konum.topleft=(30,50)

        puan2=self.oyun_font.render('2. Player Score:'+str(self.oyuncu2_puan),True,(0,50,150))
        puan2_konum=puan2.get_rect()
        puan2_konum.topleft=(GENISLIK-340,50)

        sayac_yazi=self.oyun_font.render('Remaining Time:'+str(self.sayac),True,(0,50,150))
        sayac_yazi_konum=sayac_yazi.get_rect()
        sayac_yazi_konum.topleft=(GENISLIK//2-170,50)

        pencere.blit(puan1,puan1_konum)
        pencere.blit(puan2,puan2_konum)
        pencere.blit(sayac_yazi,sayac_yazi_konum)
    def temas(self):
        if pygame.sprite.spritecollide(self.oyuncu1,self.top_grup,False):
            self.carpisma_sesi.play()
            for top in self.top_grup.sprites():
                top.yonx*=-1
                if top.hiz<=15:
                    top.hiz+=1
        if pygame.sprite.spritecollide(self.oyuncu2,self.top_grup,False):
            self.carpisma_sesi.play()
            for top in self.top_grup.sprites():
                top.yonx*=-1
                if top.hiz<=15:
                    top.hiz+=1
    def oyun_durum(self):
        for top in self.top_grup.sprites():
            if top.rect.left<=0:
                self.kenar_ses.play()
                self.oyuncu2_puan+=self.puan
            if top.rect.right>=GENISLIK:
                self.kenar_ses.play()
                self.oyuncu1_puan+=self.puan
    def bitir(self):
        bittimi=True
        global durum
        pencere.blit(self.oyun_bitti,(0,0))
        a='1. Player Won'
        b='2. Player Won'
        c='Draw'
        if self.oyuncu1_puan>self.oyuncu2_puan:
            Winner=self.oyun_font.render(a,True,(0,50,150))
            Winner_konum=Winner.get_rect()
            Winner_konum.topleft=(GENISLIK//2-150,YUKSEKLIK//4)
        if self.oyuncu2_puan>self.oyuncu1_puan:
            Winner=self.oyun_font.render(b,True,(0, 50, 150))
            Winner_konum=Winner.get_rect()
            Winner_konum.topleft=(GENISLIK//2-150,YUKSEKLIK//4)
        if self.oyuncu1_puan==self.oyuncu2_puan:
            Winner=self.oyun_font.render(c,True,(0, 50, 150))
            Winner_konum=Winner.get_rect()
            Winner_konum.topleft=(GENISLIK//2-150,YUKSEKLIK//4)
        pencere.blit(Winner,Winner_konum)
        pygame.display.update()
        while bittimi:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        self.oyun_reset()
                        bittimi=False
                if event.type==pygame.QUIT:
                    bittimi=False
                    durum=False
    def oyun_reset(self):
        self.oyuncu1_puan=0
        self.oyuncu2_puan=0
        self.sayac=30
        # Topu yeniden başlat
        for top in self.top_grup.sprites():
            top.rect.center = (GENISLIK // 2, YUKSEKLIK // 2)
            top.yonx = random.choice([-1, 1])  # Rastgele bir yön belirle
            top.yony = random.choice([-1, 1])
            top.hiz = 12  # Başlangıç hızı
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('1_oyuncu.png')
        self.rect=self.image.get_rect()
        self.rect.x=0

        #Oyuncu Değişken
        self.hiz=10
    def update(self):
        tuş=pygame.key.get_pressed()
        if tuş[pygame.K_w] and self.rect.top>5:
            self.rect.y-=self.hiz
        elif tuş[pygame.K_s] and self.rect.bottom<=YUKSEKLIK:
            self.rect.y+=self.hiz

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('2_oyuncu.png')
        self.rect=self.image.get_rect()
        self.rect.x=GENISLIK-64

        #Oyuncu Değişken
        self.hiz=10
    def update(self):
        tuş=pygame.key.get_pressed()
        if tuş[pygame.K_UP] and self.rect.top>=5:
            self.rect.y-=self.hiz
        elif tuş[pygame.K_DOWN] and self.rect.bottom<=YUKSEKLIK:
            self.rect.y+=self.hiz
class Top(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('top.png')
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y

        #Top Değişkenleri
        self.yonx=1
        self.yony=1
        self.hiz=12
    def update(self):
        self.rect.centerx+=self.hiz*self.yonx
        self.rect.centery+=self.hiz*self.yony
        if self.rect.left<=0 or self.rect.right>=GENISLIK:
            self.yonx*=-1
        if self.rect.top<=0 or self.rect.bottom>=YUKSEKLIK:
            self.yony*=-1


# 1. Oyuncu İşlemleri
oyuncu1_grup=pygame.sprite.Group()
oyuncu1=Player1()
oyuncu1_grup.add(oyuncu1)

# 2. Oyuncu işlemleri
oyuncu2_grup=pygame.sprite.Group()
oyuncu2=Player2()
oyuncu2_grup.add(oyuncu2)

# Top İşlemleri
top_grup=pygame.sprite.Group()
top=Top(random.randint(200,1000),random.randint(300,YUKSEKLIK-64))
top_grup.add(top)

#Oyun Sınıfı
oyun=Oyun(oyuncu1,oyuncu2,top_grup)
#Oyun Döngüsü
durum=True
while durum:
    for etkinlik in pygame.event.get():
        if etkinlik.type==pygame.QUIT:
            durum=False
    # Oyun İşlem Devamı
    oyun.update()
    oyun.cizdir()

    #1. Oyuncu İşlemi Devamı
    oyuncu1_grup.update()
    oyuncu1_grup.draw(pencere)

    #2. Oyuncu işlem Devamı
    oyuncu2_grup.update()
    oyuncu2_grup.draw(pencere)

    #Top İşlem Devamı
    top_grup.update()
    top_grup.draw(pencere)
    pygame.display.update()
    saat.tick(FPS)

pygame.quit()
