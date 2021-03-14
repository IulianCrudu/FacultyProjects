#include "category.h"
#include "domain.h"
#include "repository.h"
#include "service.h"
#include "ui.h"
#include "tests.h"

int main() {
    run_all_tests();

    Repository* repository = create_repository();
    Service* service = create_service(repository);
    UI* ui = create_ui(service);

    start_app(ui);
    destroy_ui(ui);
    return 0;
}