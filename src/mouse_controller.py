import pyautogui

class MouseController:
    """
    Classe responsável por controlar o mouse do computador através de comandos programáticos.
    Utiliza a biblioteca pyautogui para simular ações do mouse como movimento, cliques e scroll.
    """

    def __init__(self):
        """
        Inicializa o controlador do mouse.
        Define as dimensões da tela e variáveis de controle para os cliques.
        """
        self.screen_width, self.screen_height = pyautogui.size()
        self.has_clicked_left = False 
        self.has_clicked_right = False
        self.frames_clicked_left = 0 
        pyautogui.PAUSE = 0  # Remove delay padrão entre comandos do pyautogui

    def move_cursor(self, x, y):
        """
        Move o cursor do mouse para uma posição específica na tela.
        
        Args:
            x (float): Coordenada X normalizada (entre 0 e 1)
            y (float): Coordenada Y normalizada (entre 0 e 1)

            A detecção da mão funciona usando uma parte menor da área da tela(nesse caso, está sendo usado 60% da área central da tela, sendo considerados apenas os valores entre 0.2 e 0.8). 
            Então esse método faz uma trativa que normaliza as coordenadas entre 0.2 e 0.8 para valores entre 0 e 1.
            Assim, o usuário move a mão apenas nos 60% de área central do frame, mas o cursor do mouse consegue se mover corretamente até as bordas.
            Isso é importante pois a detecção de mão não funciona tão bem quando a mão está na borda do frame, pois ela fica parcialmente escondida.

            TODO: Considerar mover essa tratativa para fora dessa classe, já que isso sai da função de "controlar o mouse" pela qual a classe é responsável.

        """
        x = (x - 0.2) / 0.6 
        y = (y - 0.2) / 0.6 
        x = max(1, min(x * self.screen_width, self.screen_width - 2)) 
        y = max(1, min(y * self.screen_height, self.screen_height - 2)) 

        pyautogui.moveTo(x, y)

    def left_button_down(self):
        """
        Simula o pressionamento do botão esquerdo do mouse.
        Realiza um clique simples se ainda não houve clique(para prevenir cliques duplos acidentais).
        Mantém pressionado após 10 frames consecutivos.
        """
        self.frames_clicked_left += 1
        if not self.has_clicked_left:
            pyautogui.click()
            self.has_clicked_left = True
        if self.frames_clicked_left >= 10:
            pyautogui.mouseDown(button='left')

    def right_button_down(self):
        """
        Simula o pressionamento do botão direito do mouse.
        Realiza um clique direito simples se ainda não houve clique(para prevenir cliques duplos acidentais).
        """
        if not self.has_clicked_right:
            pyautogui.rightClick()
            self.has_clicked_right = True

    def buttons_up(self):
        """
        Reseta o estado dos botões do mouse.
        Libera todos os botões pressionados e zera os contadores.
        """
        self.has_clicked_right = False
        self.has_clicked_left = False
        self.frames_clicked_left = 0
        pyautogui.mouseUp(button='left')

    def scroll_down(self, scroll_value):
        """
        Realiza scroll para baixo na tela.
        
        Args:
            scroll_value (int): Quantidade de unidades para rolar para baixo
        """
        pyautogui.scroll(-scroll_value)

    def scroll_up(self, scroll_value):
        """
        Realiza scroll para cima na tela.
        
        Args:
            scroll_value (int): Quantidade de unidades para rolar para cima
        """
        pyautogui.scroll(scroll_value)
