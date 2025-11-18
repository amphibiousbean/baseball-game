using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Net.Http.Headers;

public class PythonApiService
{
    private readonly HttpClient _client;

    public PythonApiService(HttpClient client)
    {
        _client=client;
    }

    public async Task<List<Game>> Simulate(int count)
    {
        var response=await _client.GetAsync($"/simulate?count={count}");
        response.EnsureSuccessStatusCode();
        var games = await response.Content.ReadFromJsonAsync<List<Game>>();
        return games;
    }
}

