using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

public class TestController : Controller
{
    private readonly PythonApiService _pythonService;

    public TestController(PythonApiService pythonService)
    {
        _pythonService=pythonService;
    }

    public async Task<IActionResult> Simulate(int count)
    {
        var result = await _pythonService.Simulate(count);

        ViewBag.Result = result;
        return View(result);
    }
}