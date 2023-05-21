# Entrega da Atividade 2 - programação 

Nesse código, um nó chamado 'turtlecontroller' é criado para controlar o movimento de um robô simulado. O objetivo é fazer o robô seguir um caminho pré-definido.

O nó 'TurtleController' herda da classe 'Node' e é responsável por controlar o movimento do robô. Ele utiliza mensagens do ROS (Robot Operating System) para receber informações de odometria (posição e orientação) do robô e publicar comandos de velocidade por meio do Twist para o robô se mover.

O método 'pose_callback' é um callback que é chamado quando uma mensagem de odometria é recebida no tópico '/odom'. Ele recebe as informações de posição (x, y) e orientação (ângulo) da mensagem e atualiza as variáveis correspondentes no nó.

O método 'control_callback' é chamado periodicamente em um intervalo de tempo definido pelo parâmetro 'control_period'. Ele calcula a diferença entre a posição atual do robô e o próximo ponto de referência definido em 'path'. Com base nessa diferença, ele determina a velocidade linear e angular que o robô deve seguir para se aproximar do próximo ponto.

Segue o link do vídeo com a demonstração:
https://drive.google.com/file/d/1RiUWUXP6cFfaB2NLDWPWcKGHIzQGVD4F/view?usp=sharing
