import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PredictForm } from "@/components/predict-form";
import { TransactionLookup } from "@/components/transaction-lookup";

export default function Home() {
  return (
    <div className="flex flex-1 justify-center bg-muted/30 px-4 py-10">
      <main className="w-full max-w-2xl">
        <Tabs defaultValue="predict">
          <TabsList className="w-full">
            <TabsTrigger value="predict" className="flex-1">
              Evaluar
            </TabsTrigger>
            <TabsTrigger value="lookup" className="flex-1">
              Buscar
            </TabsTrigger>
          </TabsList>
          <TabsContent value="predict">
            <PredictForm />
          </TabsContent>
          <TabsContent value="lookup">
            <TransactionLookup />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
