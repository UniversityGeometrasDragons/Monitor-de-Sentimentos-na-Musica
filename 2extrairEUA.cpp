#include <iostream>
#include <fstream>
#include <regex>
#include <string>
#include <vector>
#include <map>
#include <set>

// Estrutura para armazenar os dados de uma música
struct Musica {
    std::string nomeMP3;
    std::map<std::string, double> emocoes;  // Emoções e percentuais
};

// Função para salvar os dados em um arquivo CSV
void salvarCSV(const std::vector<Musica>& dados,
               const std::vector<std::string>& emocoes, const std::string& caminhoCSV) {
    std::ofstream arquivoCSV(caminhoCSV);

    // Escrever cabeçalho do CSV
    arquivoCSV << "Arquivo MP3";
    for (const auto& emocao : emocoes) {
        arquivoCSV << "," << emocao;
    }
    arquivoCSV << "\n";

    // Escrever as linhas de dados
    for (const auto& musica : dados) {
        arquivoCSV << musica.nomeMP3;
        for (const auto& emocao : emocoes) {
            // Se a emoção não estiver presente, escreve 0
            arquivoCSV << "," << (musica.emocoes.count(emocao) ? musica.emocoes.at(emocao)/100 : 0.0);
        }
        arquivoCSV << "\n";
    }

    arquivoCSV.close();
    std::cout << "Arquivo CSV salvo com sucesso em: " << caminhoCSV << "\n";
}

int main() {
    // Abrir o arquivo HTML para leitura
    std::ifstream arquivoHTML("musicEUA.html");
    if (!arquivoHTML.is_open()) {
        std::cerr << "Erro ao abrir o arquivo HTML.\n";
        return 1;
    }

    std::string linha;
    std::regex regexDiv(R"(playx\(&quot;(.*\.mp3).*?&quot;(.*?)&quot;,\[)");
    std::regex regexEmocao(R"((\d+)% ([^,]+))");

    std::vector<Musica> dadosMusica;
    std::set<std::string> todasEmocoes;  // Usar set para evitar duplicatas

    // Ler cada linha do arquivo HTML
    while (std::getline(arquivoHTML, linha)) {
        std::smatch matchDiv;
        if (std::regex_search(linha, matchDiv, regexDiv)) {
            Musica musica;
            musica.nomeMP3 = matchDiv[1];  // Salva o nome do arquivo .mp3
            std::string emocoesStr = matchDiv[2];

            // Extrair cada emoção e seu percentual
            std::sregex_iterator iter(emocoesStr.begin(), emocoesStr.end(), regexEmocao);
            std::sregex_iterator end;
            while (iter != end) {
                std::string emocao = (*iter)[2];
                double percentual = std::stod((*iter)[1]);
                musica.emocoes[emocao] = percentual;  // Armazena no map
                todasEmocoes.insert(emocao);  // Adiciona ao conjunto de emoções
                ++iter;
            }

            // Adicionar a música à lista de dados
            dadosMusica.push_back(musica);
        }
    }

    arquivoHTML.close();

    // Converter o conjunto de emoções para um vetor ordenado
    std::vector<std::string> vetorEmocoes(todasEmocoes.begin(), todasEmocoes.end());

    // Salvar os dados extraídos em um arquivo CSV
    salvarCSV(dadosMusica, vetorEmocoes, "musicas_emocoesEUA.csv");

    return 0;
}
