from django.db import models

class Mestre(models.Model):
    nome = models.TextField(max_length=100)
    genero = models.TextField(max_length=20)
    data_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.IntegerField( help_text='Exemplo: (XX)XXXXX-XXXX / Apenas números')
    endereco = models.TextField(max_length=255, help_text='Formato: Rua, Número, Bairro')
    faixa = models.TextField(max_length=20)
    categoria = models.TextField(max_length=50)
    certificado = models.TextField(max_length=100)
    
    class Meta:
        db_table = 'mestres_table'
        app_label = 'app_teste_BD'

class Lutador(models.Model):
    # Campos do modelo
    nome = models.TextField(max_length=100)
    genero = models.TextField(max_length=20)
    data_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.IntegerField(help_text='Exemplo: (XX)XXXXX-XXXX / Apenas números')
    endereco = models.TextField(max_length=255, help_text='Formato: Rua, Número, Bairro')
    faixa = models.TextField(max_length=20)
    categoria = models.TextField(max_length=50)
    
    class Meta:
        db_table = 'lutadores_table'
        app_label = 'app_teste_BD'

class Chaveamento(models.Model):
    lutador_1 = models.ForeignKey(Lutador, related_name='lutador_1', on_delete=models.CASCADE)
    lutador_2 = models.ForeignKey(Lutador, related_name='lutador_2', on_delete=models.CASCADE)
    vencedor = models.ForeignKey(Lutador, related_name='vencedor', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lutador_1.nome} vs {self.lutador_2.nome}'

    def registrar_vencedor(self, vencedor_id):
        # Adicione a lógica para registrar o vencedor aqui
        vencedor = Lutador.objects.get(pk=vencedor_id)
        self.vencedor = vencedor
        self.save()
        
    class Meta:
        db_table = 'chaveamento'
        app_label = 'app_teste_BD'
